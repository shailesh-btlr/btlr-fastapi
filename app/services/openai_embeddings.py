import time
import json
from openai import OpenAI
from app.config import settings
# !pip install cohere tiktoken openai

client = OpenAI(api_key=settings.OPENAI_API_KEY)
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=model).data[0].embedding
    )
