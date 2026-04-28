from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from app.routes.upload import router as upload_router
from app.database import engine
from app.models import Base

app = FastAPI(title="File Upload API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://privacy-risk-frontend:3000",
        "http://172.18.0.4:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

app.include_router(upload_router, prefix="/api")
