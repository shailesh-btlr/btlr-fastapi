from app.services.graph import PreferenceGraph
#from app.services.openai_embedding import get_embedding
from app.config import settings

###
import time
import json
from openai import OpenAI


NEO4J_URL= settings.NEO4J_URI
NEO4J_PWD= settings.NEO4J_PASSWORD
NEO4J_USER= settings.NEO4J_USERNAME

client = OpenAI(api_key=settings.OPENAI_KEY)
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=model).data[0].embedding
    )
###

PreferenceGraph.set_embedding_function(get_embedding)

def semantic_search(term):
    with PreferenceGraph(NEO4J_URL, NEO4J_USER, NEO4J_PWD) as g:
      rs = g.driver.execute_query(
          # "DROP INDEX preference_embeddings"
          "CALL db.index.vector.queryNodes('p_embeddings', "
          "$numberOfNearestNeighbours, $query) "
          "YIELD node AS p, score "
          "RETURN p.id, p.path, score",
          numberOfNearestNeighbours=5,
          query=get_embedding(term)
      )
    results = [
            {"score": r["score"], "id": r["p.id"], "path": r["p.path"]}
            for r in rs.records
        ]
        
        # Convert the list of dictionaries to a JSON string
    json_result = json.dumps(results, indent=2)
        
    return results  
    


# print("--Semantic Search--")
# # semantic_search("food pizza")
# print(semantic_search("fashion dresses"))
# print(semantic_search("burger"))

# Result:
# Score ID Name
# [0.936163067817688] 47570e1d-a690-4531-a29e-eb75a5004e07 - food
# [0.9236030578613281] 9dc717dc-079e-4d8b-b8ca-74b9f41be961 - food, chicken
# [0.9181580543518066] dcd1e7cc-ac2f-4edd-88fd-5944231fb2b9 - food, chicken, spicy
# [0.8952646255493164] a7d34170-af60-436c-9ea5-9a4eaa14ede7 - sports
# [0.8833545446395874] a83d88e7-eff9-4369-a868-78f73987c2d8 - sports, water



def semantic_search_for_user(term, user):
    with PreferenceGraph(NEO4J_URL, NEO4J_USER, NEO4J_PWD) as g:
      rs = g.driver.execute_query(
          "CALL db.index.vector.queryNodes('p_embeddings', "
          "$numberOfNearestNeighbours, $query) "
          "YIELD node AS p, score "
          "MATCH (User {id: $name})-[:HAS_PREFERENCE]->(p)"
          "RETURN p.id, p.path, score",
          numberOfNearestNeighbours=50,
          name=user,
          query=get_embedding(term)
      )
    results = [
              {"score": r["score"], "id": r["p.id"], "path": r["p.path"]}
              for r in rs.records
          ]
          
          # Convert the list of dictionaries to a JSON string
    json_result = json.dumps(results, indent=2)
          
    return results    
 


# print("--Semantic Search For User--")

# print(semantic_search_for_user("dubai travel", "alyne"))
# print(semantic_search_for_user("yoga", "raj"))
# print(semantic_search_for_user("mountain", "rutuja"))

# print("For user alyne:")
# print(query1)

# print("For user raj:")
# print(query2)

# print("For user rutuja:")
# print(query3)
# Result:
# Score ID Name
# [0.9181580543518066] dcd1e7cc-ac2f-4edd-88fd-5944231fb2b9 - food, chicken, spicy
# [0.8784573078155518] 87843d7f-faa5-4ea5-bb00-9947b303186c - sports, water, swimming
