"""
Comprehensive API Validation Tests

Run with: pytest tests/test_api_validation.py -v -s

The -s flag shows print output for visibility into test values.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import storage


# Auth token for authenticated requests
AUTH_TOKEN = "mock-jwt-token-12345"
AUTH_HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}


@pytest.fixture
def client():
    """Create a test client and clear storage before each test."""
    storage.clear()
    with TestClient(app) as test_client:
        yield test_client


class TestAuthLogin:
    """POST /auth/login - Login"""

    def test_login_success(self, client):
        print("\n=== POST /auth/login - Valid credentials ===")
        response = client.post("/auth/login", json={"username": "admin", "password": "password"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert "token" in data, "Response should contain 'token'"
        assert data["token"] == "mock-jwt-token-12345", f"Token mismatch: {data['token']}"
        assert data["message"] == "Login successful", f"Message mismatch: {data['message']}"
        print("✓ Login successful with valid credentials")

    def test_login_invalid_credentials(self, client):
        print("\n=== POST /auth/login - Invalid credentials ===")
        response = client.post("/auth/login", json={"username": "wrong", "password": "wrong"})
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 401, f"Expected 401, got {response.status_code}"
        assert "invalid" in response.json()["detail"].lower()
        print("✓ Returns 401 for invalid credentials")

    def test_login_missing_fields(self, client):
        print("\n=== POST /auth/login - Missing fields ===")
        response = client.post("/auth/login", json={})
        print(f"Status: {response.status_code}")

        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print("✓ Returns 422 for missing fields")


class TestListTasks:
    """GET /tasks - List all tasks"""

    def test_list_tasks_empty(self, client):
        print("\n=== GET /tasks - Empty list ===")
        response = client.get("/tasks", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json() == [], f"Expected empty list, got {response.json()}"
        print("✓ Returns empty list initially")

    def test_list_tasks_with_data(self, client):
        print("\n=== GET /tasks - With tasks ===")
        # Create tasks
        client.post("/tasks", json={"title": "Task 1"}, headers=AUTH_HEADERS)
        client.post("/tasks", json={"title": "Task 2"}, headers=AUTH_HEADERS)

        response = client.get("/tasks", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2, f"Expected 2 tasks, got {len(data)}"
        titles = [t["title"] for t in data]
        assert "Task 1" in titles and "Task 2" in titles
        print("✓ Returns list of created tasks")

    def test_list_tasks_unauthorized(self, client):
        print("\n=== GET /tasks - Unauthorized ===")
        response = client.get("/tasks")
        print(f"Status: {response.status_code}")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print("✓ Returns 403 without auth token")


class TestCreateTask:
    """POST /tasks - Create a task"""

    def test_create_task(self, client):
        print("\n=== POST /tasks - Create task ===")
        response = client.post("/tasks", json={"title": "Buy groceries"}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        data = response.json()
        assert data["title"] == "Buy groceries", f"Title mismatch: {data['title']}"
        assert data["completed"] is False, f"Should not be completed: {data['completed']}"
        assert "id" in data, "Response should contain 'id'"
        assert "created_at" in data, "Response should contain 'created_at'"
        assert "updated_at" in data, "Response should contain 'updated_at'"
        print(f"✓ Created task with id: {data['id']}")

    def test_create_task_empty_title(self, client):
        print("\n=== POST /tasks - Empty title ===")
        response = client.post("/tasks", json={"title": ""}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print("✓ Returns 422 for empty title")

    def test_create_task_whitespace_title(self, client):
        print("\n=== POST /tasks - Whitespace title ===")
        response = client.post("/tasks", json={"title": "   "}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 422, f"Expected 422, got {response.status_code}"
        print("✓ Returns 422 for whitespace-only title")

    def test_create_task_unauthorized(self, client):
        print("\n=== POST /tasks - Unauthorized ===")
        response = client.post("/tasks", json={"title": "Test"})
        print(f"Status: {response.status_code}")

        assert response.status_code == 403, f"Expected 403, got {response.status_code}"
        print("✓ Returns 403 without auth token")


class TestGetTask:
    """GET /tasks/<id> - Get task detail"""

    def test_get_task(self, client):
        print("\n=== GET /tasks/<id> - Get task detail ===")
        # Create a task first
        create_resp = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task with id: {task_id}")

        response = client.get(f"/tasks/{task_id}", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["id"] == task_id, f"ID mismatch: {data['id']}"
        assert data["title"] == "Test task", f"Title mismatch: {data['title']}"
        assert data["completed"] is False
        print("✓ Returns task details")

    def test_get_task_not_found(self, client):
        print("\n=== GET /tasks/<id> - Not found ===")
        response = client.get("/tasks/nonexistent-id", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        assert "not found" in response.json()["detail"].lower()
        print("✓ Returns 404 for invalid ID")


class TestCompleteTask:
    """PUT /tasks/<id>/complete - Mark task as completed"""

    def test_complete_task(self, client):
        print("\n=== PUT /tasks/<id>/complete - Mark as completed ===")
        # Create a task
        create_resp = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task with id: {task_id}")
        print(f"Initial completed status: {create_resp.json()['completed']}")

        response = client.put(f"/tasks/{task_id}/complete", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert data["completed"] is True, f"Should be completed: {data['completed']}"
        print("✓ Task marked as completed")

    def test_complete_task_not_found(self, client):
        print("\n=== PUT /tasks/<id>/complete - Not found ===")
        response = client.put("/tasks/nonexistent-id/complete", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("✓ Returns 404 for invalid ID")


class TestDeleteTask:
    """DELETE /tasks/<id> - Delete a task"""

    def test_delete_task(self, client):
        print("\n=== DELETE /tasks/<id> - Delete task ===")
        # Create a task
        create_resp = client.post("/tasks", json={"title": "Task to delete"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task with id: {task_id}")

        response = client.delete(f"/tasks/{task_id}", headers=AUTH_HEADERS)
        print(f"Delete status: {response.status_code}")

        assert response.status_code == 204, f"Expected 204, got {response.status_code}"

        # Verify deletion
        get_resp = client.get(f"/tasks/{task_id}", headers=AUTH_HEADERS)
        print(f"Get after delete status: {get_resp.status_code}")
        assert get_resp.status_code == 404, "Task should not exist after deletion"
        print("✓ Task deleted successfully")

    def test_delete_task_not_found(self, client):
        print("\n=== DELETE /tasks/<id> - Not found ===")
        response = client.delete("/tasks/nonexistent-id", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 404, f"Expected 404, got {response.status_code}"
        print("✓ Returns 404 for invalid ID")


class TestTaskStats:
    """GET /tasks/stats - Return stats (total, completed, pending)"""

    def test_stats_empty(self, client):
        print("\n=== GET /tasks/stats - Empty stats ===")
        response = client.get("/tasks/stats", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0, f"Total should be 0: {data['total']}"
        assert data["completed"] == 0, f"Completed should be 0: {data['completed']}"
        assert data["pending"] == 0, f"Pending should be 0: {data['pending']}"
        print("✓ Returns zeros when no tasks")

    def test_stats_with_tasks(self, client):
        print("\n=== GET /tasks/stats - With tasks ===")
        # Create 3 tasks
        task1 = client.post("/tasks", json={"title": "Task 1"}, headers=AUTH_HEADERS).json()
        client.post("/tasks", json={"title": "Task 2"}, headers=AUTH_HEADERS)
        client.post("/tasks", json={"title": "Task 3"}, headers=AUTH_HEADERS)
        print("Created 3 tasks")

        # Complete 1 task
        client.put(f"/tasks/{task1['id']}/complete", headers=AUTH_HEADERS)
        print(f"Completed task: {task1['id']}")

        response = client.get("/tasks/stats", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        data = response.json()
        assert data["total"] == 3, f"Total should be 3: {data['total']}"
        assert data["completed"] == 1, f"Completed should be 1: {data['completed']}"
        assert data["pending"] == 2, f"Pending should be 2: {data['pending']}"
        print("✓ Returns correct stats")


class TestActivityLog:
    """GET /tasks/<id>/activity - Return activity log entries"""

    def test_activity_on_create(self, client):
        print("\n=== GET /tasks/<id>/activity - After create ===")
        create_resp = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task: {task_id}")

        response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1, f"Should have 1 entry: {len(data)}"
        assert data[0]["action"] == "created"
        assert data[0]["task_id"] == task_id
        print("✓ Activity log shows 'created' action")

    def test_activity_on_complete(self, client):
        print("\n=== GET /tasks/<id>/activity - After complete ===")
        create_resp = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        client.put(f"/tasks/{task_id}/complete", headers=AUTH_HEADERS)
        print(f"Created and completed task: {task_id}")

        response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Activity entries:")
        for entry in response.json():
            print(f"  - {entry['action']}: old={entry.get('old_value')}, new={entry.get('new_value')}")

        data = response.json()
        assert len(data) == 2, f"Should have 2 entries: {len(data)}"
        actions = [log["action"] for log in data]
        assert "created" in actions
        assert "completed" in actions
        print("✓ Activity log shows 'created' and 'completed' actions")

    def test_activity_with_values(self, client):
        print("\n=== GET /tasks/<id>/activity - With old/new values ===")
        create_resp = client.post("/tasks", json={"title": "Original"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]

        # Update via PATCH to trigger status_changed with values
        client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS)
        print(f"Created task and changed status via PATCH")

        response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
        print(f"Activity entries:")
        for entry in response.json():
            print(f"  - {entry['action']}: old_value={entry.get('old_value')}, new_value={entry.get('new_value')}")

        data = response.json()
        status_changes = [log for log in data if log["action"] == "status_changed"]
        assert len(status_changes) == 1
        assert status_changes[0]["old_value"] == "pending"
        assert status_changes[0]["new_value"] == "completed"
        print("✓ Activity log includes old_value and new_value")

    def test_activity_not_found(self, client):
        print("\n=== GET /tasks/<id>/activity - Not found ===")
        response = client.get("/tasks/nonexistent-id/activity", headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 404
        print("✓ Returns 404 for invalid ID")


class TestUpdateTask:
    """PATCH /tasks/<id> - Update task (title and/or completed)"""

    def test_update_title(self, client):
        print("\n=== PATCH /tasks/<id> - Update title ===")
        create_resp = client.post("/tasks", json={"title": "Original"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task: {task_id}, title: 'Original'")

        response = client.patch(f"/tasks/{task_id}", json={"title": "Updated"}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        assert response.json()["title"] == "Updated"
        print("✓ Title updated successfully")

    def test_update_completed(self, client):
        print("\n=== PATCH /tasks/<id> - Update completed ===")
        create_resp = client.post("/tasks", json={"title": "Test"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]
        print(f"Created task: {task_id}, completed: False")

        response = client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        assert response.status_code == 200
        assert response.json()["completed"] is True
        print("✓ Completed status updated")

    def test_update_both(self, client):
        print("\n=== PATCH /tasks/<id> - Update both fields ===")
        create_resp = client.post("/tasks", json={"title": "Original"}, headers=AUTH_HEADERS)
        task_id = create_resp.json()["id"]

        response = client.patch(f"/tasks/{task_id}", json={"title": "New Title", "completed": True}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")

        data = response.json()
        assert data["title"] == "New Title"
        assert data["completed"] is True
        print("✓ Both fields updated")

    def test_update_not_found(self, client):
        print("\n=== PATCH /tasks/<id> - Not found ===")
        response = client.patch("/tasks/nonexistent-id", json={"title": "Test"}, headers=AUTH_HEADERS)
        print(f"Status: {response.status_code}")

        assert response.status_code == 404
        print("✓ Returns 404 for invalid ID")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
