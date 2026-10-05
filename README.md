# Inventory Management System (DevOps)

A clean, modular, backend-only Inventory Management System designed for college DevOps practical examinations and viva demonstrations.

## Features

- **Product Management**: Full CRUD operations with unique SKU validation, category classification, and supplier association.
- **Supplier Management**: Full CRUD operations with contact details and product linking.
- **Stock Tracking & Transactions**: Real-time stock IN and stock OUT operations with automatic transaction logging and negative stock prevention.
- **Low Stock Detection**: Instant query for items falling below configurable threshold levels.
- **System Overview Dashboard**: Aggregate metrics for products, suppliers, total stock count, low stock warnings, and transaction totals.
- **Automated Testing**: Comprehensive pytest suite utilizing an isolated in-memory SQLite database.
- **Docker Support**: Containerized deployment with Dockerfile, Docker Compose, and persistent SQLite storage.

## Technology Stack

- **Framework**: Python 3.11+ / FastAPI
- **Database**: SQLite
- **ORM**: SQLAlchemy 2.0
- **Data Validation & Schemas**: Pydantic v2
- **Testing**: Pytest & HTTPX (FastAPI TestClient)
- **ASGI Server**: Uvicorn
- **Containerization**: Docker & Docker Compose

## Folder Structure

```text
inventory-management-devops/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── config.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── supplier.py
│   │   └── stock.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── product.py
│   │   ├── supplier.py
│   │   └── stock.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── products.py
│   │   ├── suppliers.py
│   │   ├── stock.py
│   │   └── dashboard.py
│   │
│   └── services/
│       ├── __init__.py
│       └── stock_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_products.py
│   ├── test_suppliers.py
│   ├── test_stock.py
│   └── test_dashboard.py
│
├── data/
│   └── .gitkeep
│
├── database/
│   └── init.sql
│
├── Dockerfile
├── .dockerignore
├── docker-compose.yml
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## Installation (Local Development)

1. Clone or navigate to the repository directory:
   ```bash
   cd inventory-management-devops
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows:
   .\venv\Scripts\activate
   # Linux/macOS:
   source venv/bin/activate
   ```

3. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables (optional):
   ```bash
   copy .env.example .env
   ```

## How to Run (Local)

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The database tables will be created automatically upon startup in `data/inventory.db`.

## How to Run Tests

Run the test suite using pytest:

```bash
pytest -v
```

All tests execute against an isolated in-memory SQLite database, leaving `data/inventory.db` untouched.

## Docker Support

### Concepts for Viva / Examination
- **Dockerfile**: Defines the blueprint and step-by-step instructions to build the application container image (base image, dependencies, source code, command).
- **Docker Image**: A portable, read-only package containing the application and everything it needs to run (Python runtime, libraries, source code).
- **Docker Container**: A running instance of the Docker image executed in an isolated environment.
- **Docker Compose**: A tool to define and manage multi-container Docker applications using a single YAML configuration file.
- **Docker Volume / Bind Mount (`./data:/app/data`)**: Mounts the host directory `./data` into `/app/data` inside the container, ensuring that SQLite database data persists across container restarts, updates, and recreation.

### Docker Commands

1. **Build image**:
   ```bash
   docker build -t inventory-backend:latest .
   ```

2. **Validate Compose configuration**:
   ```bash
   docker compose config
   ```

3. **Start with build**:
   ```bash
   docker compose up --build
   ```

4. **Start in background (detached mode)**:
   ```bash
   docker compose up -d
   ```

5. **Check running containers**:
   ```bash
   docker ps
   ```

6. **View container logs**:
   ```bash
   docker logs inventory-backend
   ```

7. **Stop containers**:
   ```bash
   docker compose down
   ```

## Swagger URL

Interactive OpenAPI documentation is available at:

- Local: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Docker: [http://localhost:8000/docs](http://localhost:8000/docs)
