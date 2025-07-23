#  Permit Management API – FastAPI + Celery + SQLite

A simple and extensible Permit Management system built with FastAPI. This API allows users to create permits, approve or revoke them, and automatically expire unapproved permits after 5 minutes using background tasks.

## 🔧 Features

- ✅ Create new permits (name, license plate, address)
- ✅ Approve or revoke permits via endpoints
- ✅ Filter permits by status: `pending`, `approved`, `revoked`, `expired`
- ✅ Auto-expire `pending` permits older than 5 minutes (via Celery task)
- ✅ Simple mocked token-based authentication
- ✅ SQLAlchemy ORM with PostgreSQL
- ✅ Background jobs using Celery + Redis
- ✅ Periodic tasks with Celery Beat
- ✅ Full test coverage using `pytest` + `httpx.AsyncClient`

## 🧱 Tech Stack

- **FastAPI** – High-performance Python web framework
- **SQLAlchemy** – ORM for database interaction
- **SQLite** – Database
- **Celery** – Background task queue
- **Redis** – Message broker for Celery
- **Docker & Docker Compose** – Containerized development and deployment
- **Pytest** – Testing framework

## 🚀 Getting Started

### 🔨 Requirements

- Docker
- Docker Compose

### 📦 Setup & Run (Development)

```
docker-compose up --build
```

FastAPI app will be available at: http://localhost:8000/docs

Celery worker and Redis will also start in the background.

## API Endpoints

### Auth (Mocked)
All endpoints require a mocked token:
```
Authorization: Bearer mocked-token
```
### Create Permit
``` POST /permits ```

#### Request Body
```
{
  "name": "Alice",
  "license_plate": "ABC123",
  "address": "Maple St"
}
```
#### Response
```
{
  "name": "string",
  "license_plate": "string",
  "address": "string",
  "id": 0,
  "status": "pending",
  "created_at": "2025-07-23T07:00:05.406Z"
}
```
### Approve a Permit
```
POST /permits/{id}/approve
```
### Revoke a Permit
``` 
POST /permits/{id}/revoke
```
### Get Permit
``` 
GET /permits?status=pending|approved|revoked|expired
```
## Running Tests
### To run tests:
``` 
docker-compose run web pytest
```

