from fastapi import FastAPI

app = FastAPI(title="Privacy Risk Assessment API")

@app.get("/")
def read_root():
    return {"message": "Backend is running"}
