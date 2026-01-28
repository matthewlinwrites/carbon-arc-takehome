#!/bin/bash
# ============================================
# API Validation Script
# Run backend first: uvicorn app.main:app --port 3001
# ============================================

BASE_URL="http://localhost:3001"

echo "=== 1. POST /auth/login - Login ==="
curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{"username":"admin","password":"password"}' | jq .

echo ""
echo "=== 2. GET /tasks - List all tasks (initially) ==="
curl -s "$BASE_URL/tasks" | jq .

echo ""
echo "=== 3. GET /tasks/stats - Stats (initial) ==="
curl -s "$BASE_URL/tasks/stats" | jq .

echo ""
echo "=== 4. POST /tasks - Create first task ==="
TASK1=$(curl -s -X POST "$BASE_URL/tasks" -H "Content-Type: application/json" -d '{"title":"Buy groceries"}')
echo "$TASK1" | jq .
TASK1_ID=$(echo "$TASK1" | jq -r '.id')
echo "Task 1 ID: $TASK1_ID"

echo ""
echo "=== 5. POST /tasks - Create second task ==="
TASK2=$(curl -s -X POST "$BASE_URL/tasks" -H "Content-Type: application/json" -d '{"title":"Walk the dog"}')
echo "$TASK2" | jq .
TASK2_ID=$(echo "$TASK2" | jq -r '.id')
echo "Task 2 ID: $TASK2_ID"

echo ""
echo "=== 6. GET /tasks - List all tasks ==="
curl -s "$BASE_URL/tasks" | jq .

echo ""
echo "=== 7. GET /tasks/<id> - Get task detail ==="
curl -s "$BASE_URL/tasks/$TASK1_ID" | jq .

echo ""
echo "=== 8. GET /tasks/stats - Stats after creating 2 tasks ==="
curl -s "$BASE_URL/tasks/stats" | jq .

echo ""
echo "=== 9. PUT /tasks/<id>/complete - Mark task as completed ==="
curl -s -X PUT "$BASE_URL/tasks/$TASK1_ID/complete" | jq .

echo ""
echo "=== 10. GET /tasks/stats - Stats after completing 1 task ==="
curl -s "$BASE_URL/tasks/stats" | jq .

echo ""
echo "=== 11. GET /tasks/<id>/activity - Activity log for task ==="
curl -s "$BASE_URL/tasks/$TASK1_ID/activity" | jq .

echo ""
echo "=== 12. DELETE /tasks/<id> - Delete second task ==="
curl -s -X DELETE "$BASE_URL/tasks/$TASK2_ID" -w "HTTP Status: %{http_code}\n"

echo ""
echo "=== 13. GET /tasks - List tasks after delete ==="
curl -s "$BASE_URL/tasks" | jq .

echo ""
echo "=== 14. GET /tasks/stats - Final stats ==="
curl -s "$BASE_URL/tasks/stats" | jq .

echo ""
echo "=== 15. Error cases ==="

echo ""
echo "--- GET /tasks/<invalid-id> - 404 Not Found ---"
curl -s "$BASE_URL/tasks/invalid-id-12345" | jq .

echo ""
echo "--- POST /auth/login - Invalid credentials (401) ---"
curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{"username":"wrong","password":"wrong"}' | jq .

echo ""
echo "--- POST /tasks - Empty title (422) ---"
curl -s -X POST "$BASE_URL/tasks" -H "Content-Type: application/json" -d '{"title":""}' | jq .

echo ""
echo "=== VALIDATION COMPLETE ==="
