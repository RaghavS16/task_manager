from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.auth import router as auth_router
from app.api.tasks import router as tasks_router
from app.core.config import settings
from app.db.session import init_db

app = FastAPI(
    title="Task Manager API",
    description="A simple Task Manager REST API built with FastAPI",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:8000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth_router)
app.include_router(tasks_router)

# Serve frontend static files if they exist
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")
frontend_index = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "index.html")

if os.path.isdir(frontend_dist):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

    @app.get("/", include_in_schema=False)
    def serve_frontend():
        return FileResponse(os.path.join(frontend_dist, "index.html"))

elif os.path.isfile(frontend_index):
    @app.get("/", include_in_schema=False)
    def serve_frontend_index():
        return FileResponse(frontend_index)
else:
    @app.get("/", include_in_schema=False)
    def root():
        return {"message": "Task Manager API", "docs": "/docs"}


@app.on_event("startup")
def on_startup():
    init_db()
