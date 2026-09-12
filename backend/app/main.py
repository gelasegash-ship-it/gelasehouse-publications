"""Houmba H API starter.

Run locally:
    pip install -r backend/requirements.txt
    uvicorn backend.app.main:app --reload
"""
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="Houmba H API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Publication(BaseModel):
    id: int
    title: str
    author: str
    description: str = ""
    category: str = ""
    created_at: str

class PublicationCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    author: str = Field(min_length=1, max_length=120)
    description: str = Field(default="", max_length=5000)
    category: str = Field(default="", max_length=80)

publications: List[Publication] = []

@app.get("/health")
def health():
    return {"status": "ok", "service": "houmba-h-api", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/publications", response_model=List[Publication])
def list_publications():
    return publications

@app.post("/api/publications", response_model=Publication, status_code=201)
def create_publication(payload: PublicationCreate):
    item = Publication(
        id=(publications[-1].id + 1 if publications else 1),
        created_at=datetime.now(timezone.utc).isoformat(),
        **payload.model_dump(),
    )
    publications.append(item)
    return item

@app.get("/api/publications/{publication_id}", response_model=Publication)
def get_publication(publication_id: int):
    for item in publications:
        if item.id == publication_id:
            return item
    raise HTTPException(status_code=404, detail="Publication introuvable")

@app.post("/api/ai/chat")
def ai_chat(message: str):
    return {
        "service": "Houmba H 1",
        "status": "integration_pending",
        "message": "Le connecteur IA doit être configuré avec une clé et un fournisseur autorisé.",
        "received": message,
    }
