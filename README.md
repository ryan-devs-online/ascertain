# Ascertain

A FastAPI application for managing patient records and clinical notes, with AI-powered patient summaries using Claude.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)

## Setup

1. Clone the repository
2. Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-api-key-here
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/patients
```

## Running the Application

```bash
docker compose build
docker compose up
```

The API will be available at `http://localhost:8000`.

Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

## API Overview

### Patients
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients` | List all patients (paginated) |
| POST | `/patients` | Create a new patient |
| GET | `/patients/{id}` | Get a patient by ID |
| PUT | `/patients/{id}` | Update a patient |
| DELETE | `/patients/{id}` | Delete a patient and their notes |

### Notes
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/patients/{id}/notes` | Add a clinical note for a patient |
| GET | `/patients/{id}/notes` | Get all notes for a patient |
| DELETE | `/patients/{id}/notes` | Delete all notes for a patient |

### Summary
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/patients/{id}/summary` | Generate an AI-powered clinical summary for a patient |

## Health Check

```
GET /health
```
