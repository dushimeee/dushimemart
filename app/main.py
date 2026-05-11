"""
DushimeMart - FastAPI Application Entry Point
Author: Cleonide Dushime (ID: 70871)
Course:  Introduction to Cloud Technologies — Final Project (MAX 4)

Run locally with:
    uvicorn app.main:app --reload

Then visit:
    http://localhost:8000        -> JSON welcome message
    http://localhost:8000/docs   -> Interactive Swagger UI
    http://localhost:8000/redoc  -> Alternative ReDoc UI
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app.routers import auth_router, orders_router, products_router


# Create all tables on first run (no migrations needed for this project)
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="DushimeMart API",
    description=(
        "A cloud-ready REST API for an online grocery / general store. "
        "Built with FastAPI + SQLAlchemy + JWT authentication.\n\n"
        "**Author:** Cleonide Dushime (Student ID: 70871)"
    ),
    version="1.0.0",
    contact={"name": "Cleonide Dushime", "email": "cleonide.dushime@example.com"},
)

# CORS is open for the demo — tighten this in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"], summary="Health check and welcome message")
def root():
    """Welcome endpoint — confirms the API is running."""
    return {
        "service": "DushimeMart API",
        "status": "running",
        "author": "Cleonide Dushime (ID: 70871)",
        "docs": "/docs",
    }


# Register routers
app.include_router(auth_router.router)
app.include_router(products_router.router)
app.include_router(orders_router.router)
