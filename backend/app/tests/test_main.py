## Testing for basic endpoints healthchecks

from main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    assert response.json() == {"message": "Hello World"}
    print("Response JSON:", response.json()
      )
    

