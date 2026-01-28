# Task Management Application

A full-stack task management application built with FastAPI (Python) and React (TypeScript).

## Features

- **React Router** for client-side navigation
- **Token-based authentication** - all API requests require Bearer token validation
- **Dockerized** - frontend exposed on port 3000, backend on port 3001

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

All `/tasks` endpoints require authentication via Bearer token. First, obtain a token by logging in:

| Method | Endpoint       | Description              |
|--------|----------------|--------------------------|
| POST   | `/auth/login`  | Login with credentials   |

**Login and get token:**

```bash
curl -X POST http://localhost:3001/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

**Response:**

```json
{
  "token": "mock-jwt-token-12345",
  "message": "Login successful"
}
```

### Tasks (Authentication Required)

All task endpoints require the `Authorization: Bearer <token>` header.

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
# Set your token (obtained from /auth/login)
TOKEN="mock-jwt-token-12345"

# Create a task
curl -X POST http://localhost:3001/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Buy groceries"}'

# List all tasks
curl http://localhost:3001/tasks \
  -H "Authorization: Bearer $TOKEN"

# Get a specific task
curl http://localhost:3001/tasks/{task_id} \
  -H "Authorization: Bearer $TOKEN"

# Update a task
curl -X PATCH http://localhost:3001/tasks/{task_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Buy groceries and cook dinner"}'

# Complete a task
curl -X PUT http://localhost:3001/tasks/{task_id}/complete \
  -H "Authorization: Bearer $TOKEN"

# Delete a task
curl -X DELETE http://localhost:3001/tasks/{task_id} \
  -H "Authorization: Bearer $TOKEN"

# Get task statistics
curl http://localhost:3001/tasks/stats \
  -H "Authorization: Bearer $TOKEN"
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

---

## Assumptions and Simplifications

1. **In-memory storage**: Tasks are stored in memory and reset on server restart. A production app would use a database (PostgreSQL, MongoDB, etc.).

2. **Mock authentication**: Uses a hardcoded token (`mock-jwt-token-12345`) instead of proper JWT generation/validation. A production app would use proper JWT with expiration, refresh tokens, and secure secret management.

3. **Single user**: No user management - all tasks belong to a single implicit user. A real app would have user registration, multiple users, and task ownership.

4. **Client-side pagination**: The backend returns all tasks, and pagination is handled on the frontend. For large datasets, server-side pagination with `limit`/`offset` parameters would be more efficient.

5. **No input sanitization beyond basic validation**: Title validation only checks for empty/whitespace. Production would include length limits, XSS prevention, etc.

6. **No rate limiting**: API endpoints have no rate limiting protection.

---

## Brief Questions

### How did you handle API errors?

**Backend:**
- Used FastAPI's `HTTPException` for structured error responses
- 400-level errors for client issues (401 unauthorized, 404 not found, 422 validation errors)
- Consistent error format: `{"detail": "error message"}`

**Frontend:**
- Axios interceptors catch 401 responses and redirect to login
- Components display error states using `ErrorMessage` component
- Try/catch blocks in hooks propagate errors to UI
- Loading states prevent duplicate submissions

### What tests would you write if given more time?

**Backend:**
- Integration tests with a real database
- Load/stress testing for concurrent requests
- Edge cases: very long titles, special characters, Unicode
- Rate limiting tests
- Token expiration and refresh flow tests

**Frontend:**
- Unit tests for React components (Jest + React Testing Library)
- Hook tests for `useTasks`, `useAuth`, etc.
- E2E tests with Playwright or Cypress
- Accessibility tests (axe-core)
- Visual regression tests

**General:**
- Contract testing between frontend and backend
- Security tests (SQL injection, XSS, CSRF)

### What would you improve with 1 extra hour?

1. **Filtering and sorting for tasks:**
   - Sort by `created_at`, `updated_at` (ASC/DESC)
   - Sort by `title` alphabetically (ASC/DESC)
   - Filter by `completed` status
   - Example: `GET /tasks?sort=updated_at&order=desc&completed=false`

2. **Better error handling:**
   - Toast notifications for success/error feedback
   - Retry logic for failed requests
   - Offline detection and queuing

3. **UI/UX improvements:**
   - Optimistic updates for better perceived performance
   - Confirmation dialogs before destructive actions
   - Keyboard shortcuts (Enter to save, Escape to cancel)

4. **Security hardening:**
   - Proper JWT implementation with expiration
   - HTTPS enforcement
   - Input length validation

---

## Architecture Notes

*Completed within a 2-hour time constraint.*

### Frontend Architecture

**Stack**: React 18 + TypeScript + Vite + React Router 6

**Key Design Decisions:**

1. **Context API over Redux/Zustand**
   - *Tradeoff*: Simpler setup, but limited scalability for complex state
   - *Rationale*: For a takehome with only auth state shared globally, Context is sufficient. Adding Redux would be over-engineering.

2. **Custom hooks for data fetching (`useTasks`, `useTask`, `useTaskStats`)**
   - *Tradeoff*: No built-in caching/deduplication (vs React Query/SWR)
   - *Rationale*: Keeps dependencies minimal. Manual refetch patterns are acceptable for this scope.

3. **Axios instance with interceptors** (`src/api/client.ts`)
   - *Tradeoff*: Extra abstraction layer, but centralized auth token injection and 401 handling
   - *Rationale*: Prevents token handling duplication across API calls

4. **Client-side pagination** (10 items/page in `useTasks`)
   - *Tradeoff*: Fetches all tasks then slices—doesn't scale to thousands of records
   - *Rationale*: Simpler implementation. Real production app would use server-side pagination with `limit`/`offset` query params.

5. **No automated frontend tests**
   - *Tradeoff*: Faster development, but relies on manual testing
   - *Rationale*: Acceptable for a takehome; production would add Jest + React Testing Library

### Backend Architecture

**Stack**: FastAPI + Pydantic + Uvicorn (Python 3.11)

**Key Design Decisions:**

1. **In-memory storage** (`storage.py`) instead of a database
   - *Tradeoff*: Data lost on restart, no persistence, no concurrent write safety
   - *Rationale*: Eliminates database setup complexity for reviewers. Production would use PostgreSQL/SQLite with SQLAlchemy.

2. **Mock authentication** (hardcoded `admin/password`)
   - *Tradeoff*: No real security, single user only
   - *Rationale*: Demonstrates auth flow architecture without OAuth/JWT complexity. Production would use proper JWT with expiration, refresh tokens, and password hashing.

3. **Activity logging with `old_value`/`new_value` tracking**
   - *Tradeoff*: Increases storage size, adds complexity to mutations
   - *Rationale*: Demonstrates audit trail capability—a common real-world requirement

4. **Permissive CORS (`*` origins)**
   - *Tradeoff*: Not production-safe
   - *Rationale*: Eliminates CORS debugging during development. Production would whitelist specific origins.

5. **Modular routers** (`routers/auth.py`, `routers/tasks.py`)
   - *Tradeoff*: More files to navigate
   - *Rationale*: Better separation of concerns, easier to extend. Standard FastAPI pattern.

### Docker Architecture

**Key Design Decisions:**

1. **Multi-stage frontend build** (Node builder → Nginx runtime)
   - *Tradeoff*: More complex Dockerfile, but much smaller final image (~20MB vs ~1GB)
   - *Rationale*: Production best practice. Node dependencies are build-time only.

2. **Nginx as frontend server + reverse proxy**
   - *Tradeoff*: Extra config file (`nginx.conf`) to maintain
   - *Rationale*: Solves two problems elegantly:
     - SPA routing: `try_files $uri /index.html` handles client-side routes
     - API proxying: `/api/*` → `http://backend:3001/` avoids CORS entirely in production

3. **Docker Compose service DNS** (`http://backend:3001`)
   - *Tradeoff*: Only works within Docker network
   - *Rationale*: Clean service discovery without hardcoded IPs. Frontend references backend by container name.

4. **Port mapping strategy**:
   ```
   Frontend: container:3000 → host:3000
   Backend:  container:3001 → host:3001
   ```
   - *Rationale*: Host port 3001 matches Vite dev proxy target, enabling identical API paths in dev and Docker modes.

5. **No health checks or restart policies**
   - *Tradeoff*: Container failures aren't auto-recovered
   - *Rationale*: Adds complexity. Production would add `healthcheck` and `restart: unless-stopped`.

### Tradeoffs Summary

| Decision | Benefit | Cost |
|----------|---------|------|
| No database | Zero setup for reviewers | Data volatility |
| Mock auth | Demonstrates flow without OAuth | Not production-secure |
| Client pagination | Simple hooks | Doesn't scale |
| Permissive CORS | No debugging friction | Security gap |
| Multi-stage Docker | Small images | More complex builds |
| Nginx reverse proxy | No CORS in production | Extra config |

### What Would Change for Production

1. **Database**: PostgreSQL with migrations (Alembic)
2. **Auth**: JWT with proper signing, refresh tokens, password hashing (bcrypt)
3. **Caching**: Redis for session/token storage
4. **API pagination**: Server-side with `?page=1&limit=10`
5. **Testing**: pytest-cov for backend, Jest + Playwright for frontend
6. **Docker**: Health checks, resource limits, logging drivers, secrets management
7. **CI/CD**: GitHub Actions for lint/test/build/deploy pipeline
