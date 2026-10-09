from contextlib import asynccontextmanager
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from app.config import settings
from app.database import engine, Base
import app.models  # Ensure models are imported for metadata creation
from app.routers import (
    products_router,
    suppliers_router,
    stock_router,
    dashboard_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for application startup and shutdown."""
    # Create database tables automatically
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url=None,
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Products", "description": "Operations with inventory products"},
        {"name": "Suppliers", "description": "Operations with product suppliers"},
        {"name": "Stock", "description": "Stock management and transaction logging"},
        {"name": "Dashboard", "description": "Inventory overview and metrics"},
    ],
)

# Enable Prometheus metrics
Instrumentator().instrument(app).expose(app)


# Root endpoint returning basic application information
@app.get("/", tags=["Root"])
def root():
    """Return basic application information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs_url": "/docs",
    }


# Register all routers
app.include_router(products_router)
app.include_router(suppliers_router)
app.include_router(stock_router)
app.include_router(dashboard_router)