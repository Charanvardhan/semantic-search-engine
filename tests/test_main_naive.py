import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Fixture that yields a TestClient instance wrapped in a context manager
    to correctly trigger FastAPI's on_event("startup") lifecycles.
    """
    with TestClient(app) as test_client:
        yield test_client

def test_status_endpoint(client):
    """
    Verifies that the /api/status endpoint returns a valid status and document count.
    """
    response = client.get("/api/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    # The startup hook should have automatically loaded 1,000 documents
    assert data["document_count"] == 1000
    assert data["index_type"] == "FlatL2"

def test_search_endpoint(client):
    """
    Verifies that the /api/search endpoint returns matches and calculates latency.
    """
    response = client.get("/api/search?q=technology and medical science&limit=3")
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "latency_ms" in data
    assert "results" in data
    
    results = data["results"]
    assert len(results) <= 3
    # Check schema of first search result
    if len(results) > 0:
        first_match = results[0]
        assert "id" in first_match
        assert "score" in first_match
        assert "title" in first_match
        assert "body" in first_match
        assert "category" in first_match

def test_rebuild_endpoint(client):
    """
    Verifies that triggering an index rebuild successfully updates the document count
    and returns indexing stats.
    """
    # Rebuild with 500 documents
    response = client.post("/api/index/rebuild?dataset_size=500")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "stats" in data
    assert data["stats"]["document_count"] == 500
    
    # Confirm status reflects the updated count
    status_response = client.get("/api/status")
    assert status_response.json()["document_count"] == 500
