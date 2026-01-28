def test_list_tasks_empty(client):
    """GET /tasks returns empty list initially."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_create_task(client):
    """POST /tasks creates and returns task with 201."""
    response = client.post("/tasks", json={"title": "Test task"})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test task"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_task_empty_title(client):
    """POST /tasks with empty title returns 422."""
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_whitespace_title(client):
    """POST /tasks with whitespace-only title returns 422."""
    response = client.post("/tasks", json={"title": "   "})
    assert response.status_code == 422


def test_create_task_missing_title(client):
    """POST /tasks with missing title returns 422."""
    response = client.post("/tasks", json={})
    assert response.status_code == 422


def test_get_task(client):
    """GET /tasks/{id} returns task."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"})
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test task"


def test_get_task_not_found(client):
    """GET /tasks/{id} with invalid ID returns 404."""
    response = client.get("/tasks/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_complete_task(client):
    """PUT /tasks/{id}/complete marks task as completed."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"})
    task_id = create_response.json()["id"]

    response = client.put(f"/tasks/{task_id}/complete")
    assert response.status_code == 200
    data = response.json()
    assert data["completed"] is True


def test_complete_task_not_found(client):
    """PUT /tasks/{id}/complete with invalid ID returns 404."""
    response = client.put("/tasks/nonexistent-id/complete")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_task(client):
    """DELETE /tasks/{id} removes task with 204."""
    # Create a task first
    create_response = client.post("/tasks", json={"title": "Test task"})
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204

    # Verify task is deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    """DELETE /tasks/{id} with invalid ID returns 404."""
    response = client.delete("/tasks/nonexistent-id")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_stats(client):
    """GET /tasks/stats returns correct counts."""
    # Initially all zeros
    response = client.get("/tasks/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 0
    assert data["completed"] == 0
    assert data["pending"] == 0

    # Create two tasks
    task1 = client.post("/tasks", json={"title": "Task 1"}).json()
    client.post("/tasks", json={"title": "Task 2"})

    # Complete one task
    client.put(f"/tasks/{task1['id']}/complete")

    # Check stats
    response = client.get("/tasks/stats")
    data = response.json()
    assert data["total"] == 2
    assert data["completed"] == 1
    assert data["pending"] == 1


def test_get_activity(client):
    """GET /tasks/{id}/activity returns activity log."""
    # Create a task
    create_response = client.post("/tasks", json={"title": "Test task"})
    task_id = create_response.json()["id"]

    # Get activity log
    response = client.get(f"/tasks/{task_id}/activity")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["action"] == "created"
    assert data[0]["task_id"] == task_id

    # Complete the task
    client.put(f"/tasks/{task_id}/complete")

    # Get updated activity log
    response = client.get(f"/tasks/{task_id}/activity")
    data = response.json()
    assert len(data) == 2
    actions = [log["action"] for log in data]
    assert "created" in actions
    assert "completed" in actions


def test_get_activity_not_found(client):
    """GET /tasks/{id}/activity with invalid ID returns 404."""
    response = client.get("/tasks/nonexistent-id/activity")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_list_tasks_after_create(client):
    """GET /tasks returns list of created tasks."""
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    titles = [task["title"] for task in data]
    assert "Task 1" in titles
    assert "Task 2" in titles
