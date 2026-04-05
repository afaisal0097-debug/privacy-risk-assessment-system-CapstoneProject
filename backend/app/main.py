from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.database import engine
from app.models import Base

app = FastAPI(title="File Upload API")

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(upload_router, prefix="/api")
