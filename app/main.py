"""Main FastAPI application."""

from fastapi import FastAPI

from app.database import Base, engine
from app.routes import appointment_router, doctor_router, patient_router

# Create all database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Hospital Management API",
    description="API for managing patients, doctors, and appointments",
    version="0.1.0",
)

# Include routers
app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Welcome to Hospital Management API",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
