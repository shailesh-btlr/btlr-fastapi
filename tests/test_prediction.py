
from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)

def test_query_extract_preferences_success():
    input_str = "I prefer vegetarian food and like to travel to Europe."
    expected_output = {
        "diet": "vegetarian",
        "travel_destination": "Europe"
        }
    response = client.post("/query_extract_preferences", json={"input_str": input_str})
    assert response.status_code == 200
    assert response.json() == expected_output

def test_query_extract_preferences_failure():

    input_str = ""  
    response = client.post("/query_extract_preferences", json={"input_str": input_str})
    assert response.status_code == 400
    assert "detail" in response.json()