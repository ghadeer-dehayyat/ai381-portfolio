# AI381 Lab 2: Container and CI

[![CI](https://github.com/ghadeer-dehayyat/ai381-portfolio/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ghadeer-dehayyat/ai381-portfolio/actions/workflows/ci.yml)

A machine learning churn prediction API packaged with Docker and automated using GitHub Actions. The project demonstrates model serving, automated testing, container security scanning, and publishing Docker images to GitHub Container Registry (GHCR).

## Project Overview

This project packages a machine learning churn prediction model as a REST API using FastAPI.

It includes:

- A model-serving API with `/health` and `/predict` endpoints.
- Pydantic-based input validation.
- Automated tests using pytest.
- A multi-stage Docker image running as a non-root user.
- A Docker health check.
- GitHub Actions CI/CD automation.
- Trivy vulnerability scanning.
- Automatic publishing to GitHub Container Registry (GHCR), tagged with the commit SHA.

## Project Structure

```text
lab-02/
├── src/
│   ├── app/
│   │   └── main.py
│   └── train/
│       └── train.py
├── tests/
│   └── test_api.py
├── model.joblib
├── requirements.txt
├── requirements-dev.txt
├── Dockerfile
├── .dockerignore
├── sample_request.json
└── README.md
```

## Requirements

- Python 3.14
- Docker Desktop with WSL2, or a compatible Docker environment
- Git

## Run Locally

Open a terminal in the `labs/lab-02` directory.

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows CMD:

```cmd
.venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 3. Start the API

Run the service with one command:

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks whether the API is running and the model is loaded. |
| POST | `/predict` | Returns a churn prediction for the supplied input. |

The `/predict` endpoint validates incoming data using Pydantic before making a prediction.

See `sample_request.json` for an example request payload.

## Run Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The test suite contains at least five tests covering:

- Health endpoint behavior.
- Model loading.
- Prediction endpoint contract.
- Invalid input validation.
- Unexpected input fields.

## Code Quality

Run Ruff to check code quality:

```bash
ruff check src tests
```

## Docker

The Dockerfile uses a multi-stage build to separate dependency installation from the runtime image.

It also includes:

- A pinned Python base image.
- A non-root application user.
- A Docker `HEALTHCHECK`.
- A production-style Uvicorn startup command.

### Build the image

Run from the `labs/lab-02` directory:

```bash
docker build -t ai381-churn-api:local .
```

### Run the container

```bash
docker run --rm -p 8000:8000 ai381-churn-api:local
```

The API will be available at http://localhost:8000.

## CI/CD Pipeline

GitHub Actions automates the testing, building, scanning, and publishing process.

### Pull Requests

When a pull request targets `main`, the workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs development dependencies.
4. Runs Ruff linting.
5. Runs the pytest test suite.

### Pushes to Main

When changes are pushed to `main`, the workflow:

1. Runs the tests and lint checks.
2. Builds the Docker image.
3. Scans the image using Trivy.
4. Pushes the image to GHCR if the scan succeeds.

All third-party GitHub Actions are pinned to full commit SHAs.

## Docker Image on GHCR

The published image is available through GitHub Container Registry.

**Package:** `ai381-churn-api`

**Registry:** `ghcr.io`

**Package visibility:** Public

[View the Docker package on GHCR](https://github.com/users/ghadeer-dehayyat/packages/container/ai381-churn-api)

Pull the published image using its commit-SHA tag:

```bash
docker pull ghcr.io/ghadeer-dehayyat/ai381-churn-api:0e3db81d56fabc9b2ef74373bdf2668746f2741a
```

**Image digest:** `ADD_VERIFIED_GHCR_IMAGE_DIGEST_HERE`

## Repository

[GitHub Repository](https://github.com/ghadeer-dehayyat/ai381-portfolio)

---

**AI381 Lab 2 – Container and CI**  
Faculty of Computer and Information Technology  
Jordan University of Science and Technology (JUST)
