from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
import os
from typing import Dict, Any

from app.routes.upload import router as upload_router
from app.database import engine
from app.models import Base

try:
    from fastapi.staticfiles import StaticFiles
except Exception:
    StaticFiles = None

try:
    from app.uniqueness import uniqueness_and_rare_combination
except Exception:
    uniqueness_and_rare_combination = None


app = FastAPI(title="Privacy Risk Assessment API")

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

# Create database tables
Base.metadata.create_all(bind=engine)

# Register existing upload routes
app.include_router(upload_router, prefix="/api")


# Find project root
# main.py is usually inside backend/app/main.py
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

results_dir = os.path.join(repo_root, "results")
webapp_dir = os.path.join(repo_root, "frontend", "webpage")


# Serve generated CSV result files
if StaticFiles is not None:
    if os.path.isdir(results_dir):
        app.mount("/results", StaticFiles(directory=results_dir), name="results")

    if os.path.isdir(webapp_dir):
        app.mount("/webapp", StaticFiles(directory=webapp_dir, html=True), name="webapp")


@app.get("/")
def root() -> Dict[str, str]:
    return {
        "message": "Privacy Risk Assessment API is running"
    }


@app.get("/api/list-results")
def list_results() -> Dict[str, Any]:
    if not os.path.isdir(results_dir):
        return {"files": []}

    files = [
        file_name
        for file_name in sorted(os.listdir(results_dir))
        if file_name.lower().endswith(".csv")
    ]

    return {"files": files}


@app.get("/api/run-uniqueness")
def run_uniqueness() -> Dict[str, Any]:
    if uniqueness_and_rare_combination is None:
        return {
            "success": False,
            "message": "uniqueness_and_rare_combination function is not available"
        }

    result = uniqueness_and_rare_combination()

    return {
        "success": True,
        "uniqueness_score_pct": result.get("uniqueness_score_pct"),
        "rare_combination_score_pct": result.get("rare_combination_score_pct"),
        "result": result,
    }


if __name__ == "__main__":
    if uniqueness_and_rare_combination is None:
        print("uniqueness_and_rare_combination function is not available")
    else:
        s = uniqueness_and_rare_combination()
        print("uniqueness_score_pct:", s["uniqueness_score_pct"])
        print("rare_combination_score_pct:", s["rare_combination_score_pct"])