import unittest
from unittest.mock import MagicMock

from app.config import settings
from app.services.graph import PrefereceGraphException, PreferenceGraph

NEO4J_URI = settings.NEO4J_URI
NEO4J_USER = settings.NEO4J_USERNAME
NEO4J_PASS = settings.NEO4J_PASSWORD

USER = "TSTUSR999"


class PreferenceGraphTestCase(unittest.TestCase):
    def setUp(self):
        PreferenceGraph.set_embedding_function(MagicMock(return_value=[]))
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            g.driver.execute_query("MATCH (n) DETACH DELETE n")
        self.maxDiff = None

    def test_bootstrap(self):
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            g.bootstrap(["Food"])
            records, _, _ = g.driver.execute_query(
                "MATCH (n) RETURN count(n) AS count"
            )
            self.assertEqual(2, records[0]["count"])  # root + cluster node

    def test_setup_user(self):
        self.test_bootstrap()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            g.setup_user(USER)
            preferences = g.get_preferences_for_user(USER)
            self.assertEqual(
                [
                    ["root", "Food"],
                ],
                sorted([[p["name"] for p in ps] for ps in preferences]),
            )

    def test_add_preference(self):
        self.test_setup_user()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            preferences = g.get_preferences_for_user(USER)
            g.add_preference_to_user(USER, preferences[0][1]["id"], "Chicken")
            updated_preferences = g.get_preferences_for_user(USER)
            self.assertEqual(
                [
                    ["root", "Food", "Chicken"],
                ],
                sorted(
                    [[p["name"] for p in ps] for ps in updated_preferences]
                ),
            )

    def test_get_preference_tree_for_user(self):
        self.test_add_preference()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            tree = g.get_preference_tree_for_user(USER)
            self.assertEqual(tree["name"], "root")
            self.assertEqual(tree["children"][0]["name"], "Food")
            self.assertEqual(
                tree["children"][0]["children"][0]["name"], "Chicken"
            )  # noqa: E501

    def test_add_preference_tree_for_user_identity(self):
        self.test_add_preference()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            tree = g.get_preference_tree_for_user(USER)
            # tree["children"].append(dict(name="newcluster"))
            g.add_preference_tree_to_user(tree, USER)
            # self.assertEqual(tree,2)

    def test_add_preference_tree_for_user_expansion(self):
        self.test_add_preference()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            tree = g.get_preference_tree_for_user(USER)
            tree["children"][0]["children"].append(
                dict(name="fruit", children=[dict(name="apple", children=[])])
            )
            # the next call modifies `tree` and assigns IDs to the new children
            # thus `updated_tree` and `tree` will be equal
            g.add_preference_tree_to_user(tree, USER)
            updated_tree = g.get_preference_tree_for_user(USER)
            self.assertEqual(tree, updated_tree)

    @unittest.skip(
        "Decission not to restrict nodes directly connected to root."
    )
    def test_add_preference_tree_for_user_exception(self):
        self.test_add_preference()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            tree = g.get_preference_tree_for_user(USER)
            tree["children"].append(dict(name="newcluster"))
            with self.assertRaises(PrefereceGraphException):
                g.add_preference_tree_to_user(tree, USER)

    def test_unlink_preference(self):
        self.test_add_preference()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            preferences = g.get_preferences_for_user(USER)
            g.unlink_preference_from_user(USER, preferences[0][2]["id"])
            updated_preferences = g.get_preferences_for_user(USER)
            self.assertEqual(
                [
                    ["root", "Food"],
                ],
                sorted(
                    [[p["name"] for p in ps] for ps in updated_preferences]
                ),
            )

    def test_embedding(self):
        self.test_setup_user()
        embedding_function = MagicMock(return_value=[])
        PreferenceGraph.set_embedding_function(embedding_function)
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            preferences = g.get_preferences_for_user(USER)
            g.add_preference_to_user(USER, preferences[0][1]["id"], "Chicken")
            updated_preferences = g.get_preferences_for_user(USER)
            self.assertEqual(
                [
                    ["root", "Food", "Chicken"],
                ],
                sorted(
                    [[p["name"] for p in ps] for ps in updated_preferences]
                ),
            )
            embedding_function.assert_called_once_with("food, chicken")

    def test_add_preference_path_error(self):
        self.test_bootstrap()
        with PreferenceGraph(NEO4J_URI, NEO4J_USER, NEO4J_PASS) as g:
            g.bootstrap(["Food"])
            with self.assertRaises(PrefereceGraphException):
                g.add_preference_path_to_user(["Food", "Chicken"], USER)


if __name__ == "__main__":
    unittest.main()
