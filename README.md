# Task Management Application

A full-stack task management application built with FastAPI (Python) and React (TypeScript).

## Project Structure

```
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── models.py        # Pydantic data models
│   │   ├── schemas.py       # Request/response schemas
│   │   ├── storage.py       # In-memory storage
│   │   └── routers/         # API route handlers
│   ├── tests/               # Pytest test suite
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── api/             # API client modules
│   │   ├── components/      # React components
│   │   ├── context/         # React context providers
│   │   ├── hooks/           # Custom hooks
│   │   ├── pages/           # Page components
│   │   └── types/           # TypeScript types
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
│
└── docker-compose.yml       # Docker orchestration
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker & Docker Compose (optional)

---

## Running Locally

### Backend

1. **Create and activate a virtual environment:**

   ```bash
   cd backend
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start the development server:**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 3001
   ```

   The API will be available at `http://localhost:3001`

4. **View API documentation:**

   - Swagger UI: http://localhost:3001/docs
   - OpenAPI JSON: http://localhost:3001/openapi.json

### Frontend

1. **Install dependencies:**

   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server:**

   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

---

## Running with Docker

The easiest way to run the full application:

```bash
docker-compose up --build
```

This starts both services:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:3001

To run in detached mode:

```bash
docker-compose up -d --build
```

To stop:

```bash
docker-compose down
```

---

## Testing

### Backend Tests

Run the full test suite:

```bash
cd backend
source .venv/bin/activate
pytest
```

**Common test commands:**

```bash
# Verbose output
pytest -v

# Run a specific test file
pytest tests/test_auth.py -v

# Run a specific test function
pytest tests/test_tasks.py::test_create_task -v

# Show print statements in output
pytest -v -s

# Run with coverage (if pytest-cov is installed)
pytest --cov=app
```

**Example test output:**

```
$ pytest -v
========================= test session starts ==========================
collected 15 items

tests/test_auth.py::test_login_success PASSED
tests/test_auth.py::test_login_invalid_credentials PASSED
tests/test_tasks.py::test_create_task PASSED
tests/test_tasks.py::test_get_all_tasks PASSED
tests/test_tasks.py::test_complete_task PASSED
...
========================= 15 passed in 0.45s ===========================
```

### Frontend Tests

```bash
cd frontend

# Lint the codebase
npm run lint

# Type check
npx tsc --noEmit
```

### API Validation Script

A shell script is available for manual API testing:

```bash
cd backend/tests
chmod +x validate_api.sh
./validate_api.sh
```

---

## API Endpoints

### Authentication

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| POST   | `/auth/login`  | Login with credentials   |

**Example:**

```bash
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Tasks

| Method | Endpoint                   | Description            |
|--------|----------------------------|------------------------|
| GET    | `/tasks`                   | List all tasks         |
| POST   | `/tasks`                   | Create a new task      |
| GET    | `/tasks/{task_id}`         | Get a specific task    |
| PATCH  | `/tasks/{task_id}`         | Update a task          |
| PUT    | `/tasks/{task_id}/complete`| Mark task as complete  |
| DELETE | `/tasks/{task_id}`         | Delete a task          |
| GET    | `/tasks/{task_id}/activity`| Get task activity log  |
| GET    | `/tasks/stats`             | Get task statistics    |

**Examples:**

```bash
# Create a task
curl -X POST http://localhost:3001/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'

# List all tasks
curl http://localhost:3001/tasks

# Get a specific task
curl http://localhost:3001/tasks/{task_id}

# Update a task
curl -X PATCH http://localhost:3001/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries and cook dinner"}'

# Complete a task
curl -X PUT http://localhost:3001/tasks/{task_id}/complete

# Delete a task
curl -X DELETE http://localhost:3001/tasks/{task_id}

# Get task statistics
curl http://localhost:3001/tasks/stats
```

---

## Development Notes

### Default Credentials

For development/testing, use:
- **Username:** `admin`
- **Password:** `password`

### Storage

The application uses **in-memory storage** - all data is lost when the server restarts. This is intentional for development purposes.

### Frontend Proxy

In development mode, the frontend proxies `/api` requests to the backend. This is configured in `frontend/vite.config.ts`.

### CORS

The backend allows all origins in development. Adjust `app/main.py` for production use.

---

## Build for Production

### Backend

```bash
cd backend
docker build -t task-api .
docker run -p 3001:3001 task-api
```

### Frontend

```bash
cd frontend
npm run build        # Outputs to dist/
npm run preview      # Preview the production build locally
```

Or with Docker:

```bash
docker build -t task-frontend .
docker run -p 3000:3000 task-frontend
```
