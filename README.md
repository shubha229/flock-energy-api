# Urja Meter Ops API

A Python FastAPI service that provides a clean API interface over the existing Urja Meter Ops portal. It exposes meter search, location, and energy-reading endpoints without modifying the portal.

## Features

- Health check endpoint.
- Search meters by query with pagination.
- Retrieve a meter's geographic location.
- Retrieve energy readings for a meter.
- Automatic API documentation through Swagger UI.
- Centralized portal authentication and error handling.

## Tech Stack

- Python
- FastAPI
- Requests
- Pydantic
- Uvicorn
- Pytest

## Project Structure

```text
flock-energy-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── client.py
│   ├── main.py
│   └── models.py
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── openapi.json
├── PROTOCOL.md
├── README.md
├── REFLECTION.md
└── requirements.txt
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/shubha229/flock-energy-api
cd flock-energy-api
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example environment file to `.env`:

```powershell
Copy-Item .env.example .env
```

Open `.env` and replace the placeholder values with the portal credentials provided for the assignment.

Example configuration:

```env
PORTAL_BASE_URL=https://urja-ops.flockenergy.tech
PORTAL_USERNAME=your_portal_username
PORTAL_PASSWORD=your_portal_password
```

Keep `.env` local. Never commit portal credentials, session cookies, or other secrets to GitHub.

## Run the API

```bash
uvicorn app.main:app --reload --reload-dir app
```

Once running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- Health check: `http://127.0.0.1:8000/health`

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/meters?q=&page=1` | Search meters with pagination |
| GET | `/meters/{meter_id}/location` | Retrieve meter coordinates |
| GET | `/meters/{meter_id}/energy` | Retrieve energy readings |

## Error Handling

- Invalid meter IDs return a 404 response when the upstream portal indicates that the meter was not found.
- Upstream portal failures are translated into API error responses.
- Invalid pagination parameters are rejected by the API.

### Example requests

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Search meters:

```bash
curl "http://127.0.0.1:8000/meters?q=J100000&page=1"
```

Retrieve location:

```bash
curl http://127.0.0.1:8000/meters/J100000/location
```

Retrieve energy readings:

```bash
curl http://127.0.0.1:8000/meters/J100000/energy
```

The API response schemas and exact response examples can be inspected in Swagger UI at `/docs`.

## Testing

Run the automated tests:

```bash
python -m pytest -v
```

The current test suite covers the health endpoint, meter search, page validation, location and energy retrieval, and invalid meter IDs.

## Documentation

- [PROTOCOL.md](PROTOCOL.md): Observed portal behavior, authentication, endpoints, and assumptions.
- [openapi.json](openapi.json): OpenAPI specification generated from the FastAPI application.
- [REFLECTION.md](REFLECTION.md): Assignment reflection and engineering decisions.

## Assumptions and Trade-offs

- The existing portal remains the source of truth for meter information.
- The API uses the portal's observed authentication and session behavior.
- The service provides a small set of useful endpoints instead of reproducing every portal feature.
- Portal errors are translated into API errors rather than exposing internal credentials or session details.
- The implementation prioritizes clarity and a working, testable integration over additional infrastructure.

## What I Intentionally Skipped

I focused on the core meter search, location, and energy endpoints to keep the implementation manageable and testable. I did not implement a complete network hierarchy API, a local indexing layer, caching, or a separate frontend. These features would require additional investigation and testing, so I documented them as possible improvements rather than expanding the scope before the core service was working.

## Limitations and Future Improvements

- Add stronger handling for expired portal sessions and authentication retries.
- Add configurable caching where appropriate.
- Expand automated tests with mocked upstream responses and additional failure scenarios.
- Investigate and document additional portal endpoints, including meter hierarchy information, if required.
- Add structured logging and more detailed operational monitoring.

## Assignment Deliverables

- API source code
- `README.md`
- `PROTOCOL.md`
- `openapi.json`
- `REFLECTION.md`
