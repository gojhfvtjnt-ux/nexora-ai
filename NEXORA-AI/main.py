
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse

from ai_writer.writer import router as writer_router
from ai_business.business import router as business_router

app = FastAPI(
    title="NEXORA AI",
    description="One platform. Many possibilities.",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent

@app.get("/")
def home():
    return FileResponse(BASE_DIR / "index.html")

app.include_router(writer_router)
app.include_router(business_router)

@app.get("/writer")
def writer_page():
    return FileResponse(BASE_DIR / "frontend" / "writer.html")

@app.get("/business")
def business_page():
    return FileResponse(BASE_DIR / "frontend" / "business.html")