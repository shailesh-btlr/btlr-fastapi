import time
import json
from openai import OpenAI
from app.config import settings
# !pip install cohere tiktoken openai

client = OpenAI(api_key=settings.OPENAI_KEY)
def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return (
        client.embeddings.create(input=[text], model=model).data[0].embedding
    )

VECTOR_DIMENSIONS = len(get_embedding("Hello World"))

INSTRUCTIONS = """
Task: Categorize a range of user preferences into a hierarchical tree structure.
Guidelines:
Exclude verbs & conjunctions from all hierarchy formations.
Place main action of of preference as the starting point of the hierarchical tree.
Basic Hierarchy Formation: Begin with the broadest category and drill down to specifics. E.g., "I like tomatoes in my salad but not in a sandwich" becomes:
Food, Salad, Tomato
Food, Sandwich, No Tomato
Complex Inputs: For nuanced statements, ensure the hierarchy captures the entire context. E.g., "I enjoy walking my dog in the park, it gives me positive vibes" becomes:
Activities, Outdoor, Park, Walk, Dog
Emotion, Positive, Park, Walk, Dog
Notice that both preferences as they are both referring to the dog and then should end with the same item so that they maintain the same context.
Complex Input with simultaneous events: For nuanced statements, merge parallel hierarchy's together. E.g., "I enjoy eating burgers while watching insta reels" Hierarchy:
Food, eating, burger
Entertainment, social media, instagram, watching, reels
becomes:
Food, eating, burger, entertainment, social media, instagram, watching, reels
No Preference Statements: If a statement lacks a clear preference, ask a follow-up question. E.g., "Did you mean [inferred preference]?"
Contradictory Preferences: For contradictory statements, prioritize one clear preference. E.g., "I prefer reading fiction, not non-fiction" becomes:
Activity, Reading, Fiction
Relationship Preferences: If a preference involves relationships, reflect this in the hierarchy. E.g., "I like to go away with my family to surf" becomes:
Activities, Holiday, Outdoor, Beach, Surfing
Relationship, Family, Holiday, Beach, Surfing
Neutral Sentiment: Maintain a neutral tone, focusing solely on categorization without sentiment.
Output Format for every message:
Structure your response as a JSON object.
Include "follow_up_question" for clarification requests leaving the preferences blank but ensure its in the JSON format.
Ensure the JSON output is complete, leaving irrelevant fields blank.
Stem the words and return them as lowercase unless they are brand names such as IBM, SAP im which case use the capitalization as commonly used with the brand.
Return the json response as plain string and nothing else.
Example Output:
{
  "follow_up_question": "Did you mean to say you enjoy outdoor activities on weekends?",
  "preferences": [
    ["activity", "holiday", "no beach"],
    ["time", "weekday", "sunday"]
  ]
}
"""

assistant = client.beta.assistants.create(
    name="Preference Classifier",
    instructions=INSTRUCTIONS,
    model="gpt-4-1106-preview"
)

def extract_preferences(statement):
  thread = client.beta.threads.create()
  message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user", #@title dds
    content=statement
  )
  run = client.beta.threads.runs.create(
      thread_id=thread.id,
      assistant_id=assistant.id
  )
  while client.beta.threads.runs.retrieve(
      thread_id=thread.id,
      run_id=run.id
      ).completed_at is None:
     time.sleep(1)
  response = client.beta.threads.messages.list(
      thread_id=thread.id
  ).data[0].content[0].text.value
  return json.loads(response)

# print("Testing extract_preferences...")
# print(extract_preferences("I prefer people on Earth. Don't like those skinny Marsians"))
