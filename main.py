from fastapi import FastAPI
from routers import invoice_router
from database import Base, engine
import models  # noqa: F401 - registers SQLAlchemy models before create_all

app = FastAPI(
    title="AI Invoice Generator",
    version="1.0.0",
    description="AI-powered invoice extraction, validation, masking and PDF generation API.",
)

# Create tables after models are imported.
Base.metadata.create_all(bind=engine)

app.include_router(invoice_router.router, prefix="/api", tags=["Invoice"])


@app.get("/")
def root():
    return {
        "message": "AI Invoice Generator is running!",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}
