from fastapi import APIRouter, HTTPException
from typing import Optional
from app.services.query_extract_preferences import extract_preferences
from app.services.semantic_search_graph import semantic_search, semantic_search_for_user
from app.services.query_vectordb import vectordb_search,add_documents_to_qdrant
from pydantic import BaseModel
from typing import List
from langchain.schema import Document


router = APIRouter()

@router.post("/query-extract-preferences")
async def query_extract_preferences(input_str: str) -> dict:
  """
  Extract preferences from the provided string.

  Args:
      input_str (str): The input string from which preferences will be extracted.

  Returns:
      dict: A dictionary containing the extracted preferences.

  Raises:
      HTTPException: If the extraction fails or the input is invalid.
  """
  try:
      extracted_preferences = extract_preferences(input_str)
      return extracted_preferences
  except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
  



@router.post("/graph-semantic-search")
async def search(term: str, user: Optional[str] = None):
    """
    Semantic search endpoint that supports both general search and user-specific search.
    
    Parameters:
    - term: Search term (required)
    - user: Username (optional)
    
    Returns:
    - List of search results with scores, IDs, and paths
    """
    try:
        if user:
            results = semantic_search_for_user(term, user)
            return {
                "status": "success",
                "type": "user_specific_search",
                "user": user,
                "term": term,
                "results": results
            }
        else:
            results = semantic_search(term)
            return {
                "status": "success",
                "type": "general_search",
                "term": term,
                "results": results
            }
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    
@router.post("/query-vectordb-qa")

async def search(query: str, k: Optional[int] = None):  
    """
    Search the vector database with a given query and return the results.

    Args:
      query (str): The search query string.
      k (Optional[int]): The number of top results to return. Defaults to None, which may imply returning all results.

    Returns:
      dict: The search results from the vector database.

    Raises:
      HTTPException: If an error occurs during the search process, an HTTP 400 error is raised with the error details.
    """
    try:
       vectordb_search_result = vectordb_search(query,k)
       return vectordb_search_result
    except Exception as e:
      raise HTTPException(status_code=400, detail=str(e))
    


class DocumentData(BaseModel):
  page_content: str
  metadata: dict

class AddDocumentsRequest(BaseModel):
  documents: List[DocumentData]

@router.post("/add-documents-vectordb/")
async def add_documents(request: AddDocumentsRequest):
  try:
      documents = [Document(page_content=doc.page_content, metadata=doc.metadata) for doc in request.documents]
      result = add_documents_to_qdrant(
          documents=documents
      )
      return result
  except Exception as e:
      raise HTTPException(status_code=500, detail=str(e))    