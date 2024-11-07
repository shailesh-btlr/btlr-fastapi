import getpass
import os
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from uuid import uuid4
from langchain_core.documents import Document
from app.config import settings


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