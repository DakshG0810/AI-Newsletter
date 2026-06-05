from fastapi import FastAPI
from app.models.article import Article
from app.database import Base, engine
from app.models.subscriber import Subscriber
from app.routes.subscribers import router as subscriber_router
from app.routes.newsletters import router as news_router
from app.models.newsletter import Newsletter
from fastapi.middleware.cors import CORSMiddleware
from app.services.scheduler import (
    start_scheduler
)
# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Newsletter API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8080"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Register routes
app.include_router(subscriber_router)
app.include_router(news_router)
@app.get("/")
def root():
    return {
        "message": "AI Newsletter Backend Running"
    }
@app.on_event("startup")
def startup_event():

    start_scheduler()