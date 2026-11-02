# AI381 Lab 2: Container and CI

[![CI](https://github.com/ghadeer-dehayyat/ai381-portfolio/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ghadeer-dehayyat/ai381-portfolio/actions/workflows/ci.yml)

A machine learning churn prediction API packaged with Docker and automated using GitHub Actions. This project demonstrates model serving, automated testing, containerization, security scanning, and continuous integration and delivery (CI/CD).

## Project Overview

This project packages a trained customer churn prediction model as a REST API using FastAPI.

The API accepts customer information and returns the predicted probability of churn.

### Key Features

- FastAPI REST API with `/health` and `/predict` endpoints.
- Pydantic input validation.
- Machine learning model loading using Joblib.
- Automated testing using pytest.
- Multi-stage Docker build.
- Non-root container execution.
- Docker HEALTHCHECK.
- Automated linting and testing with GitHub Actions.
- Docker image vulnerability scanning using Trivy.
- Automatic image publishing to GitHub Container Registry (GHCR), tagged with the commit SHA.

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

### 1. Create a virtual environment

```bash
python -m venv .venv
```

### 2. Activate the virtual environment

Windows CMD:

```cmd
.venv\Scripts\activate
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Start the API

Run the service with one command:

```bash
uvicorn src.app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at:

- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## API Endpoints

The application provides two endpoints:

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Checks API availability and model loading status. |
| POST | `/predict` | Predicts the probability of customer churn. |

### Health Check

Request:

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "model_loaded": true
}
```

### Churn Prediction

Request:

```http
POST /predict
Content-Type: application/json
```

Example request body:

```json
{
  "tenure_months": 5,
  "monthly_fee": 89.9,
  "contract": "month-to-month",
  "internet_service": "fiber",
  "support_calls": 3
}
```

Example response:

```json
{
  "churn_probability": 0.735
}
```

*The probability shown above is illustrative. The actual result is calculated by the trained model.*

### Input Validation

The API uses Pydantic to validate customer input before making predictions.

| Field | Validation |
|---|---|
| `tenure_months` | Non-negative integer |
| `monthly_fee` | Non-negative number |
| `contract` | Non-empty string |
| `internet_service` | Non-empty string |
| `support_calls` | Non-negative integer |

Unexpected input fields are rejected using `ConfigDict(extra="forbid")`.

## Run Tests

Run the automated test suite:

```bash
python -m pytest -v
```

The test suite contains at least five tests covering:

1. Health endpoint behavior.
2. Model loading.
3. Prediction endpoint contract.
4. Invalid input validation.
5. Unexpected input fields.

## Code Quality

Run Ruff to check code quality:

```bash
ruff check src tests
```

## Docker

The Dockerfile uses a multi-stage build to separate dependency installation from the runtime environment.

It includes:

- A pinned Python base image.
- Separate builder and runtime stages.
- A non-root application user.
- A Docker HEALTHCHECK.
- A Uvicorn startup command.

### Build the Docker Image

Run from the `labs/lab-02` directory:

```bash
docker build -t ai381-churn-api:local .
```

### Run the Container

```bash
docker run --rm -p 8000:8000 ai381-churn-api:local
```

The API will be available at:

http://localhost:8000

### Check Container Health

```bash
docker ps
```

The container health status can be checked using:

```bash
docker inspect --format="{{.State.Health.Status}}" CONTAINER_ID
```

## Security Scanning with Trivy

Trivy is used to scan the Docker image for vulnerabilities.

The GitHub Actions workflow scans for HIGH and CRITICAL vulnerabilities and fails the pipeline if matching findings are detected.

Local scan example:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock aquasec/trivy:latest image --scanners vuln --severity HIGH,CRITICAL --ignore-unfixed ai381-churn-api:local
```

## CI/CD Pipeline

GitHub Actions automates testing, Docker image building, vulnerability scanning, and publishing.

### Pull Requests

When a pull request targets the `main` branch, the workflow:

1. Checks out the repository.
2. Sets up Python.
3. Installs development dependencies.
4. Runs Ruff linting.
5. Runs the pytest test suite.

### Pushes to Main

When changes are pushed to `main`, the workflow:

1. Runs linting and tests.
2. Builds the Docker image.
3. Scans the image using Trivy.
4. Pushes the image to GitHub Container Registry if the scan succeeds.

All third-party GitHub Actions are pinned to full commit SHAs.

## Docker Image on GitHub Container Registry (GHCR)

The Docker image is published to GitHub Container Registry.

- **Package:** `ai381-churn-api`
- **Registry:** `ghcr.io`
- **Visibility:** Public

[View the Docker package on GHCR](https://github.com/users/ghadeer-dehayyat/packages/container/ai381-churn-api)

### Pull the Image Using Its Commit SHA Tag

```bash
docker pull ghcr.io/ghadeer-dehayyat/ai381-churn-api:0e3db81d56fabc9b2ef74373bdf2668746f2741a
```

### Image Digest

```text
sha256:9c9498d101a706cf2b0b73c5678082abfab80c40dd6f4e28e1f1aca61a51070a
```

Pull the exact image by digest:

```bash
docker pull ghcr.io/ghadeer-dehayyat/ai381-churn-api@sha256:9c9498d101a706cf2b0b73c5678082abfab80c40dd6f4e28e1f1aca61a51070a
```

## Repository

[GitHub Repository](https://github.com/ghadeer-dehayyat/ai381-portfolio)

---

**AI381 Lab 2 - Container and CI**  
Faculty of Computer and Information Technology  
Jordan University of Science and Technology (JUST)

## Development Workflow

All changes are submitted through pull requests.

Pull requests targeting `main` must pass the required
GitHub Actions checks before they can be merged.

The `main` branch is protected by repository rules.
