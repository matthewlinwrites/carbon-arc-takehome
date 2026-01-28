AUTH_TOKEN = "mock-jwt-token-12345"
AUTH_HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}


def test_list_tasks_empty(client):
    """GET /tasks returns empty list initially."""
    response = client.get("/tasks", headers=AUTH_HEADERS)
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    """POST /tasks creates and returns task with 201."""
    response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_empty_title(client):
    """POST /tasks with empty title returns 422."""
    response = client.post("/tasks", json={"title": ""}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_create_task_whitespace_title(client):
    """POST /tasks with whitespace-only title returns 422."""
    response = client.post("/tasks", json={"title": "   "}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_create_task_missing_title(client):
    """POST /tasks with missing title returns 422."""
    response = client.post("/tasks", json={}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_get_task(client):
    """GET /tasks/{id} returns task."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test task"


def test_get_task_not_found(client):
    """GET /tasks/{id} with invalid ID returns 404."""
    response = client.get("/tasks/nonexistent-id", headers=AUTH_HEADERS)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_complete_task(client):
    """PUT /tasks/{id}/complete marks task as completed."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/complete", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_complete_task_not_found(client):
    """PUT /tasks/{id}/complete with invalid ID returns 404."""
    response = client.put("/tasks/nonexistent-id/complete", headers=AUTH_HEADERS)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_task(client):
    """DELETE /tasks/{id} removes task with 204."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}", headers=AUTH_HEADERS)
    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}", headers=AUTH_HEADERS)
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """DELETE /tasks/{id} with invalid ID returns 404."""
    response = client.delete("/tasks/nonexistent-id", headers=AUTH_HEADERS)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_stats(client):
    """GET /tasks/stats returns correct counts."""
    # Initially all zeros
    response = client.get("/tasks/stats", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["completed"] == 0
    assert data["pending"] == 0

    # Create two tasks
    task1 = client.post("/tasks", json={"title": "Task 1"}, headers=AUTH_HEADERS).json()
    client.post("/tasks", json={"title": "Task 2"}, headers=AUTH_HEADERS)

    # Complete one task
    client.put(f"/tasks/{task1['id']}/complete", headers=AUTH_HEADERS)

    # Check stats
    response = client.get("/tasks/stats", headers=AUTH_HEADERS)
    data = response.json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1


def test_get_activity(client):
    """GET /tasks/{id}/activity returns activity log."""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    # Get activity log
    response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["action"] == "created"
    assert data[0]["task_id"] == task_id

    # Complete the task
    client.put(f"/tasks/{task_id}/complete", headers=AUTH_HEADERS)

    # Get updated activity log
    response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
    data = response.json()
    assert len(data) == 2
    actions = [log["action"] for log in data]
    assert "created" in actions
    assert "completed" in actions


def test_get_activity_not_found(client):
    """GET /tasks/{id}/activity with invalid ID returns 404."""
    response = client.get("/tasks/nonexistent-id/activity", headers=AUTH_HEADERS)
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_tasks_after_create(client):
    """GET /tasks returns list of created tasks."""
    client.post("/tasks", json={"title": "Task 1"}, headers=AUTH_HEADERS)
    client.post("/tasks", json={"title": "Task 2"}, headers=AUTH_HEADERS)

    response = client.get("/tasks", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles


# PATCH /tasks/{id} tests
def test_update_task_title(client):
    """PATCH /tasks/{id} updates task title."""
    create_response = client.post("/tasks", json={"title": "Original title"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"title": "Updated title"}, headers=AUTH_HEADERS
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["completed"] is False


def test_update_task_completed(client):
    """PATCH /tasks/{id} updates task completed status."""
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True
    assert data["title"] == "Test task"


def test_update_task_toggle_back_to_pending(client):
    """PATCH /tasks/{id} can toggle completed back to false."""
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    # Mark as complete
    client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS)

    # Toggle back to pending
    response = client.patch(
        f"/tasks/{task_id}", json={"completed": False}, headers=AUTH_HEADERS
    )
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is False


def test_update_task_both_fields(client):
    """PATCH /tasks/{id} can update both title and completed."""
    create_response = client.post("/tasks", json={"title": "Original"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": "New title", "completed": True},
        headers=AUTH_HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "New title"
    assert data["completed"] is True


def test_update_task_not_found(client):
    """PATCH /tasks/{id} with invalid ID returns 404."""
    response = client.patch(
        "/tasks/nonexistent-id", json={"title": "Test"}, headers=AUTH_HEADERS
    )
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_task_empty_title(client):
    """PATCH /tasks/{id} with empty title returns 422."""
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.patch(f"/tasks/{task_id}", json={"title": ""}, headers=AUTH_HEADERS)
    assert response.status_code == 422


def test_update_task_whitespace_title(client):
    """PATCH /tasks/{id} with whitespace-only title returns 422."""
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}", json={"title": "   "}, headers=AUTH_HEADERS
    )
    assert response.status_code == 422


# Activity log with old_value/new_value tests
def test_activity_log_has_status_change_values(client):
    """Activity log includes old_value and new_value for status changes."""
    create_response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    # Change status via PATCH
    client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS)

    response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()

    # Find the status change entry
    status_changes = [log for log in data if log["action"] == "status_changed"]
    assert len(status_changes) == 1
    assert status_changes[0]["old_value"] == "pending"
    assert status_changes[0]["new_value"] == "completed"


def test_activity_log_has_title_change_values(client):
    """Activity log includes old_value and new_value for title changes."""
    create_response = client.post("/tasks", json={"title": "Original title"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    # Change title
    client.patch(f"/tasks/{task_id}", json={"title": "New title"}, headers=AUTH_HEADERS)

    response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()

    # Find the title update entry
    updates = [log for log in data if log["action"] == "updated"]
    assert len(updates) == 1
    assert updates[0]["old_value"] == "Original title"
    assert updates[0]["new_value"] == "New title"


def test_activity_log_multiple_changes(client):
    """Activity log tracks multiple changes correctly."""
    create_response = client.post("/tasks", json={"title": "Task"}, headers=AUTH_HEADERS)
    task_id = create_response.json()["id"]

    # Make multiple changes
    client.patch(f"/tasks/{task_id}", json={"title": "Updated Task"}, headers=AUTH_HEADERS)
    client.patch(f"/tasks/{task_id}", json={"completed": True}, headers=AUTH_HEADERS)
    client.patch(f"/tasks/{task_id}", json={"completed": False}, headers=AUTH_HEADERS)

    response = client.get(f"/tasks/{task_id}/activity", headers=AUTH_HEADERS)
    data = response.json()

    # Should have: created, updated (title), status_changed (to completed), status_changed (to pending)
    assert len(data) == 4
    actions = [log["action"] for log in data]
    assert actions.count("created") == 1
    assert actions.count("updated") == 1
    assert actions.count("status_changed") == 2


def test_task_fields_structure(client):
    """Task response contains required fields: id, title, completed."""
    response = client.post("/tasks", json={"title": "Test task"}, headers=AUTH_HEADERS)
    assert response.status_code == 201
    data = response.json()

    # Required fields per spec
    assert "id" in data
    assert "title" in data
    assert "completed" in data
    assert isinstance(data["id"], str)
    assert isinstance(data["title"], str)
    assert isinstance(data["completed"], bool)


def test_stats_fields_structure(client):
    """Stats response contains total, completed, and pending fields."""
    response = client.get("/tasks/stats", headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()

    assert "total" in data
    assert "completed" in data
    assert "pending" in data
    assert isinstance(data["total"], int)
    assert isinstance(data["completed"], int)
    assert isinstance(data["pending"], int)
