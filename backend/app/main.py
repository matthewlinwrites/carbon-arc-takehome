from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, tasks

app = FastAPI(
    title="Task Management API",
    description="A RESTful API for task management",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks.router)
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Task Management API", "docs": "/docs"}
