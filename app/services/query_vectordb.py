import getpass
import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from uuid import uuid4
from langchain_core.documents import Document
from app.config import settings
from typing import List
from qdrant_client.http.models import Distance, VectorParams




os.environ["OPENAI_API_KEY"] = settings.OPENAI_KEY
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

docs = []
url = settings.QDRANT_URL
api_key = settings.QDRANT_URL_API_KEY



def vectordb_search(collection_name:str,query:str,k:int):
   qdrant = QdrantVectorStore.from_existing_collection(
      embedding=embeddings,
      collection_name=collection_name,
      url=url,
      api_key=api_key,
      )
   
   results = qdrant.similarity_search(query,k = k)
   results_list = [
      {
      "metadata": res.metadata,
      "page_content": res.page_content
      }
      for res in results
      ]
   return results_list




def add_documents_to_qdrant(documents: List[Document],collection_name:str):
  try:
      client = QdrantClient(
         url=url,
         api_key=api_key,)
      
      # Retrieve the list of collections
      collections = client.get_collections()
      print(collections)
      collection_exists = any(collection.name == collection_name for collection in collections.collections)
      if collection_exists:
         print(collection_name)
      else:   
         qdrant = QdrantVectorStore.from_documents(
            docs,
            embeddings,
            url=url,
            prefer_grpc=True,
            api_key=api_key,
            collection_name=collection_name,
            )
      
      qdrant = QdrantVectorStore.from_existing_collection(
         embedding=embeddings,
         collection_name=collection_name,
         url=url,
         api_key=api_key,
         )
      uuids = [str(uuid4()) for _ in range(len(documents))]
      qdrant.add_documents(documents=documents, ids=uuids)
      return {"status": "success", "message": "Documents added successfully","uuids": uuids}
  except Exception as e:
     print(f"Error in add_documents_to_qdrant. Error Messege: {str(e)}")


def get_collection_name():
   client = QdrantClient(
         url=url,
         api_key=api_key,)
      
   # Retrieve the list of collections
   collections = client.get_collections()
   collection_names = [collection.name for collection in collections.collections]
   return collection_names

get_collection_name()