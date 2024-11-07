import openai
from app.config import settings

client = openai.OpenAI(
    api_key=settings.OPENAI_KEY,
)


def generate_gpt_response(prompt, max_tokens=8000):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response.choices[0].message.content


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=model).data[0].embedding
    )
