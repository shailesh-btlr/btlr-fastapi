from neo4j import GraphDatabase


class PrefereceGraphException(Exception):
    pass


class PreferenceGraph:
    ROOT_NODE_ID = "0"
    _embedding_function = None

    def __init__(self, uri, username, password):
        if PreferenceGraph._embedding_function is None:
            raise PrefereceGraphException(
                "PreferenceGraph embedding_function is not set. "
                "Please call set_embedding_function() first."
            )
        self.uri = uri
        self.username = username
        self.password = password

    def __enter__(self):
        self.driver = GraphDatabase.driver(
            self.uri, auth=(self.username, self.password)
        )
        self.driver.verify_connectivity()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @classmethod
    def set_embedding_function(cls, f):
        cls._embedding_function = f

    def close(self):
        self.driver.close()

    def bootstrap(self, clusters):
        self.driver.execute_query(
            "CREATE CONSTRAINT unique_preference_id IF NOT EXISTS "
            "FOR (p:Preference) REQUIRE p.id IS UNIQUE"
        )
        self.driver.execute_query(
            "CREATE CONSTRAINT unique_user_id  IF NOT EXISTS "
            "FOR (u:User) REQUIRE u.id IS UNIQUE"
        )
        self.driver.execute_query(
            "CREATE VECTOR INDEX preference_embeddings IF NOT EXISTS "
            "FOR (p: Preference) ON (p.embedding) "
            "OPTIONS "
            "{indexConfig: { "
            "  `vector.dimensions`: 384, "
            "  `vector.similarity_function`: 'cosine' "
            "}}"
        )
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                tx.run(
                    "MERGE (:Preference {name: 'root', id: $root_node_id})",
                    root_node_id=self.ROOT_NODE_ID,
                )
                for cluster in clusters:
                    self.create_preference_tx(tx, self.ROOT_NODE_ID, cluster)

    @staticmethod
    def create_preference_tx(tx, parent_id, name):
        existing_preference = PreferenceGraph.find_child_node_by_name_tx(
            tx, parent_id, name
        )
        if not existing_preference:
            return tx.run(
                "MATCH (p:Preference {id: $parent_id}) "
                "CREATE (p)<-[:HAS_PARENT]-(new:Preference {name: $name, id: randomUUID(), embedding: $embedding}) "  # noqa: E501
                "RETURN (new.id) AS id",
                parent_id=parent_id,
                name=name,
                embedding=PreferenceGraph._embedding_function(
                    ", ".join(
                        list(
                            node["name"].lower()
                            for node in PreferenceGraph.get_path(
                                tx, PreferenceGraph.ROOT_NODE_ID, parent_id
                            )[1:]
                        )
                        + [name.lower()]
                    )
                ),
            ).single()["id"]
        else:
            return existing_preference["p"]["id"]

    @staticmethod
    def get_path(tx, from_id, to_id):
        if from_id == to_id:
            return []
        return tx.run(
            "MATCH path = (:Preference {id: $from_id})<-[*]-(:Preference {id: $to_id}) "  # noqa: E501
            "RETURN nodes(path) as path_nodes ",
            from_id=from_id,
            to_id=to_id,
        ).single()["path_nodes"]

    @staticmethod
    def find_child_node_by_name_tx(tx, parent_id, name):
        return tx.run(
            "MATCH (p:Preference)-[:HAS_PARENT]->(:Preference {id: $parent_id}) "  # noqa: E501
            "WHERE toUpper(p.name) = toUpper($name) "
            "RETURN (p) ",
            parent_id=parent_id,
            name=name,
        ).single()

    def setup_user(self, user_id):
        self.driver.execute_query(
            "CREATE (u:User {id:$user_id}) "  # FIXME this should be a create
            "WITH u "
            "MATCH (p:Preference)-[:HAS_PARENT]->(:Preference {id:$root_node_id}) "  # noqa: E501
            "MERGE (u)-[:HAS_PREFERENCE]-> (p) ",
            user_id=user_id,
            root_node_id=self.ROOT_NODE_ID,
        )

    def add_preference_to_user(self, user_id, parent_id, name):
        with self.driver.session() as session:
            with session.begin_transaction() as tx:
                preference_id = self.create_preference_tx(tx, parent_id, name)
                tx.run(
                    "MATCH (u:User {id: $user_id}) "
                    "MATCH (p:Preference {id: $new_id}) "
                    "MERGE (u)-[:HAS_PREFERENCE]->(p) "
                    "WITH u "
                    "MATCH (u)-[r:HAS_PREFERENCE]->(:Preference {id: $parent_id}) "  # noqa: E501
                    "DELETE (r) ",
                    parent_id=parent_id,
                    user_id=user_id,
                    new_id=preference_id,
                )
                return preference_id

    def add_preference_path_to_user(self, path, user_id):
        if not path[0].lower() == "root":
            raise PrefereceGraphException(
                "Preference path must start with 'root'"
            )
        parent_id = self.ROOT_NODE_ID
        for segment in path:
            parent_id = self.add_preference_to_user(
                user_id, parent_id, segment
            )

    def add_preference_tree_to_user(self, tree, user_id):
        parent_id = tree["id"]
        for child in tree["children"]:
            id = self.add_preference_to_user(user_id, parent_id, child["name"])
            child["id"] = id
            self.add_preference_tree_to_user(child, user_id)

    def unlink_preference_from_user(self, user_id, preference_id):
        return self.driver.execute_query(
            "MATCH (u:User {id: $user_id}) "
            "-[r:HAS_PREFERENCE]->(:Preference {id: $preference_id}) "
            "-[:HAS_PARENT]->(parent:Preference) "
            "-[:HAS_PARENT*1..]->(:Preference {id: $root_node_id}) "  # *1 to disallow clusters to be deleted  # noqa: E501
            "DELETE r "
            "MERGE (u)-[:HAS_PREFERENCE]->(parent) ",
            user_id=user_id,
            preference_id=preference_id,
            root_node_id=self.ROOT_NODE_ID,
        ).summary.counters.contains_updates

    def get_preferences_for_user(self, user_id):
        result = self.driver.execute_query(
            "MATCH path = (:Preference {id: $root_node_id})<-[*]-(:User {id: $user_id}) "  # noqa: E501
            "RETURN nodes(path) as path_nodes ",
            root_node_id=self.ROOT_NODE_ID,
            user_id=user_id,
        )
        return [
            [
                dict((k, v) for k, v in node.items() if k != "embedding")
                for node in record["path_nodes"][
                    :-1
                ]  # -1 to drop the user node  # noqa: E501
            ]
            for record in result.records
        ]

    def get_preference_tree_for_user(self, user_id):
        def lookup(dictionaries, matcher, default=None):
            return next(
                (
                    d
                    for d in dictionaries
                    if all(d[key] == matcher[key] for key in matcher)
                ),
                default,
            )

        preference_paths = self.get_preferences_for_user(user_id)
        tree = dict(name="fakeroot", children=[])

        for path in preference_paths:
            children = tree["children"]
            for node in path:
                matched_child = lookup(children, dict(name=node["name"]))
                if matched_child is None:
                    new_child = dict(**node, children=[])
                    children.append(new_child)
                    children = new_child["children"]
                else:
                    children = matched_child["children"]

        if tree["children"]:
            return tree["children"][0]
