[![codecov](https://codecov.io/gh/asacristani/fastapi-k8s/branch/main/graph/badge.svg)](https://codecov.io/gh/tu-usuario/tu-repo)

# 🛡️ Insurance Claims API

Simple RESTful API built with FastAPI to manage insurance claims.
This project demonstrates good backend engineering practices, including TDD, authentication, CI/CD, Kubernetes deployment, and observability.


## 📦 Features

- ✅ RESTful API to create, retrieve and manage insurance claims
- 🔐 JWT-based authentication (register/login)
- 🧪 TDD-first development with Pytest
- 🐳 Docker + docker-compose for local development
- ☸️ Kubernetes manifests for deployment
- 🔁 GitHub Actions CI/CD pipeline
- 📊 Basic observability with logs and Prometheus metrics

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone git@github.com:asacristani/fastapi-k8s.git
cd fastapi-k8s
```

### 2. Create environment variables

Create a .env file:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=claims_db
DATABASE_URL=postgresql://postgres:postgres@db:5432/claims_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```


### 3. Run the application
Using Docker Compose:

```bash
docker-compose up --build
```
The API will be available at http://localhost:8000.

## 📚 API Documentation

Once running, visit:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 Authentication

Endpoints:
- `POST /auth/register` – Create a new user
- `POST /auth/login` – Retrieve a JWT token
- `GET /auth/me` - Get the user data

Use the Authorization: Bearer <token> header to access protected routes.

## 📝 Claims Endpoints

- `POST /claims` – Submit a new insurance claim
- `GET /claims` – List all claims for the current user
- `GET /claims/{id}` – Get a specific claim
- `PUT /claims/{id}` – Update claim status or data
- `DELETE /claims/{id}` – Delete a claim

## ✅ Code Quality and Testing

This project uses a pre-commit pipeline and CI to enforce code quality and test coverage.

### 🧪 Run tests with coverage

```bash
pytest --cov=app --cov-report=term-missing
```

### 🧹 Code formatting and linting
We use:

- black – code formatter
- flake8 – syntax/style linter
- isort – import sorter

Run them all via pre-commit:

```bash
# One-time install
pip install pre-commit
pre-commit install

# Run on all files
pre-commit run --all-files
```

These checks are also executed automatically on each git commit and in the CI pipeline.

### ⚙️ Continuous Integration

GitHub Actions will automatically:

- Run pre-commit checks
- Run tests with pytest and coverage report

CI workflow located at: `.github/workflows/ci.yml`

## ☸️ Kubernetes
To deploy the app to Kubernetes:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

The deployment includes readiness and liveness probes.
