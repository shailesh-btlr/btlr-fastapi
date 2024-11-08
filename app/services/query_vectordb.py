import getpass
import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from uuid import uuid4
from langchain_core.documents import Document
from app.config import settings
from typing import List
from qdrant_client.http.models import PointStruct




os.environ["OPENAI_API_KEY"] = settings.OPENAI_KEY
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

docs = []
url = settings.QDRANT_URL
api_key = settings.QDRANT_URL_API_KEY

qdrant = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,
    collection_name="my_documents",
    url=url,
    api_key=api_key,
)

def vectordb_search(query,k):
   results = qdrant.similarity_search(query,k = k)
   results_list = [
      {
      "metadata": res.metadata,
      "page_content": res.page_content
      }
      for res in results
      ]
   return results_list




def add_documents_to_qdrant(documents: List[Document]):
  uuids = [str(uuid4()) for _ in range(len(documents))]
  qdrant.add_documents(documents=documents, ids=uuids)
  return {"status": "success", "message": "Documents added successfully","uuids": uuids}