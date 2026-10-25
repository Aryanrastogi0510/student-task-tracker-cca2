import pytest
from app import app, tasks

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def setup_function():
    tasks.clear()
    tasks.extend([
        {"id": 1, "title": "Sample task", "done": False},
        {"id": 2, "title": "Completed task", "done": True},
    ])

def test_home_page_shows_tasks(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Task Tracker" in response.data
    assert b"Sample task" in response.data

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_add_task(client):
    response = client.post("/tasks", data={"title": "Study Docker"})
    assert response.status_code == 302
    assert any(task["title"] == "Study Docker" for task in tasks)

def test_toggle_task(client):
    client.post("/tasks/1/toggle")
    assert tasks[0]["done"] is True
