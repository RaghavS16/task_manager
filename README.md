# TaskFlow – Task Manager

A full-stack Task Manager built with **FastAPI** (backend) and plain **HTML/CSS/JS** (frontend). Features JWT authentication, SQLite/PostgreSQL support, pagination, and filtering.

**Live Demo:** _https://your-deployment-url.onrender.com_  
**API Docs:** _https://your-deployment-url.onrender.com/docs_

---

## Features

- User registration & login (JWT-based auth, bcrypt password hashing)
- Create, view, update, and delete tasks
- Mark tasks as completed
- Pagination and filtering (`?completed=true/false`)
- Task isolation — users only see their own tasks
- Single-file frontend served by FastAPI
- SQLite (dev) / PostgreSQL (production) support
- Pytest test suite with 15+ test cases
- Docker support

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py        # /register, /login endpoints
│   │   │   ├── tasks.py       # /tasks CRUD endpoints
│   │   │   └── deps.py        # JWT dependency injection
│   │   ├── core/
│   │   │   ├── config.py      # Settings (pydantic-settings)
│   │   │   └── security.py    # JWT + bcrypt utilities
│   │   ├── db/
│   │   │   └── session.py     # SQLAlchemy engine + session
│   │   ├── models/
│   │   │   ├── user.py        # User ORM model
│   │   │   └── task.py        # Task ORM model
│   │   ├── schemas/
│   │   │   ├── user.py        # Pydantic schemas for users
│   │   │   └── task.py        # Pydantic schemas for tasks
│   │   ├── tests/
│   │   │   └── test_main.py   # Pytest test suite
│   │   └── main.py            # FastAPI app entry point
│   ├── requirements.txt
│   ├── pytest.ini
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   └── index.html             # Single-page frontend app
├── Dockerfile                 # Full-stack Docker build
├── .gitignore
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | No | Register new user |
| POST | `/login` | No | Login, returns JWT |
| POST | `/tasks` | Yes | Create a task |
| GET | `/tasks` | Yes | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | Yes | Get single task |
| PUT | `/tasks/{id}` | Yes | Update task |
| DELETE | `/tasks/{id}` | Yes | Delete task |
| GET | `/docs` | No | Swagger UI |

**Query parameters for `GET /tasks`:**
- `page` — page number (default: 1)
- `size` — items per page (default: 10, max: 100)
- `completed` — filter by status: `true` or `false`

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp backend/.env.example backend/.env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | _(required)_ | JWT signing secret — use a long random string |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token TTL in minutes |
| `DATABASE_URL` | `sqlite:///./taskmanager.db` | Database connection string |
| `FRONTEND_URL` | `http://localhost:3000` | Allowed CORS origin |

**Generate a strong SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Local Setup

### Prerequisites
- Python 3.11+
- pip

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/yourusername/taskmanager.git
cd taskmanager

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependencies
cd backend
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and set SECRET_KEY

# 5. Run the server
uvicorn app.main:app --reload --port 8000
```

Open **http://localhost:8000** for the frontend app.  
Open **http://localhost:8000/docs** for the Swagger UI.

---

## Running Tests

```bash
cd backend
pytest
```

The test suite uses an in-memory SQLite test database (auto-created and destroyed per test session).

---

## Docker

### Build & Run (full-stack)

```bash
docker build -t taskmanager .
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=sqlite:///./taskmanager.db \
  taskmanager
```

### Backend only

```bash
cd backend
docker build -t taskmanager-api .
docker run -p 8000:8000 -e SECRET_KEY=your-secret-key taskmanager-api
```

---

## Deployment (Render)

1. Push to a public GitHub repo
2. Create a new **Web Service** on [Render](https://render.com)
3. Set **Build Command:** `pip install -r backend/requirements.txt`
4. Set **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set environment variables in Render dashboard:
   - `SECRET_KEY` — generate with `python -c "import secrets; print(secrets.token_hex(32))"`
   - `DATABASE_URL` — use `sqlite:///./taskmanager.db` for SQLite, or add a PostgreSQL database from Render
   - `FRONTEND_URL` — your Render app URL

---

## Deployment (Railway)

```bash
railway login
railway init
railway add
railway up
```

Set env vars in the Railway dashboard.

---

## Usage

1. Open the hosted URL
2. Click **Register** and create an account
3. Log in with your credentials
4. Create tasks using the form at the top
5. Click the circle button to mark a task complete
6. Use filters (All / Pending / Completed) to sort your view
7. Click **delete** to remove a task
