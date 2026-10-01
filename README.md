# OrderFlow

OrderFlow is a backend order management project built with FastAPI and PostgreSQL.

It provides REST APIs for creating, retrieving, and updating orders, with database persistence, schema migrations, automated tests, and a Docker-based local development environment.

## Tech Stack

### Backend
- Python 3.12
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL
- Alembic

### Development & Testing
- Docker / Docker Compose
- pytest
- Ruff
- uv

## Features

### Order Management
- Create orders
- List orders
- Get an order by ID
- Update order status
- Validate supported order statuses

### Backend & Data
- PostgreSQL data persistence
- SQLAlchemy ORM
- Alembic database migrations
- Docker-based local PostgreSQL environment

### Quality
- Automated API tests with pytest
- Code quality checks with Ruff
- Interactive API documentation with FastAPI Swagger UI

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| GET | `/health` | Health check |
| POST | `/orders` | Create an order |
| GET | `/orders` | List orders |
| GET | `/orders/{id}` | Get an order by ID |
| PATCH | `/orders/{id}/status` | Update order status |

Supported order statuses:

- `pending`
- `processing`
- `completed`
- `cancelled`

## Local Setup

```bash
docker compose up -d
cp backend/.env.example backend/.env

cd backend
uv sync
uv run alembic upgrade head
uv run fastapi dev
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Tests

```bash
uv run pytest
uv run ruff check .
```

## Planned Improvements

- Order filtering and pagination
- External commerce channel integrations
- Webhook-based order ingestion
- Automated SMS notifications with Twilio
- Frontend dashboard