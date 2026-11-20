
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI(
    title="NEXORA AI",
    description="One platform. Many possibilities.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")
