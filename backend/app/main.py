"""Houmba H API: publication platform foundation with authentication and AI gateway."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, hmac, json, secrets
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from .config import get_settings

settings = get_settings()
app = FastAPI(title="Houmba H API", version="1.0.0", description="Backend de la plateforme HOUMBA H et de Houmba H 1")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(',') if x.strip()], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

DATA_FILE = Path(__file__).resolve().parent.parent / "houmba_data.json"

def load_data():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    return {"users": [], "publications": [], "tokens": {}}

def save_data(data):
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

data = load_data()

class RegisterIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class PublicationIn(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=10000)
    category: str = Field(default="Général", max_length=80)
    cover_url: Optional[str] = None

class CommentIn(BaseModel):
    text: str = Field(min_length=1, max_length=2000)

def password_hash(password: str, salt: str | None = None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 120000).hex()
    return f"{salt}${digest}"

def password_ok(password, stored):
    salt, digest = stored.split('$', 1)
    return hmac.compare_digest(password_hash(password, salt).split('$', 1)[1], digest)

def current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(401, 'Authentification requise')
    token = authorization[7:]
    user_id = data['tokens'].get(token)
    user = next((u for u in data['users'] if u['id'] == user_id), None)
    if not user: raise HTTPException(401, 'Session invalide')
    return user

@app.get('/health')
def health():
    return {'status':'ok','service':'houmba-h-api','version':'1.0.0','timestamp':datetime.now(timezone.utc).isoformat()}

@app.post('/api/auth/register', status_code=201)
def register(payload: RegisterIn):
    if any(u['email'].lower() == payload.email.lower() for u in data['users']): raise HTTPException(409, 'Cet email existe déjà')
    user = {'id': secrets.token_hex(8), 'name': payload.name, 'email': payload.email.lower(), 'password_hash': password_hash(payload.password), 'created_at': datetime.now(timezone.utc).isoformat()}
    data['users'].append(user); save_data(data)
    return {'id':user['id'], 'name':user['name'], 'email':user['email']}

@app.post('/api/auth/login')
def login(payload: LoginIn):
    user = next((u for u in data['users'] if u['email'] == payload.email.lower()), None)
    if not user or not password_ok(payload.password, user['password_hash']): raise HTTPException(401, 'Email ou mot de passe incorrect')
    token = secrets.token_urlsafe(32); data['tokens'][token] = user['id']; save_data(data)
    return {'access_token':token, 'token_type':'bearer', 'user':{'id':user['id'],'name':user['name'],'email':user['email']}}

@app.get('/api/me')
def me(user=Depends(current_user)):
    return {'id':user['id'],'name':user['name'],'email':user['email'],'created_at':user['created_at']}

@app.get('/api/publications')
def list_publications(q: Optional[str]=None, category: Optional[str]=None):
    items = list(reversed(data['publications']))
    if q: items = [p for p in items if q.lower() in (p['title']+' '+p['description']).lower()]
    if category: items = [p for p in items if p['category'].lower() == category.lower()]
    return items

@app.post('/api/publications', status_code=201)
def create_publication(payload: PublicationIn, user=Depends(current_user)):
    item = {'id':secrets.token_hex(8),'title':payload.title,'description':payload.description,'category':payload.category,'cover_url':payload.cover_url,'author':{'id':user['id'],'name':user['name']},'likes':0,'comments':[],'created_at':datetime.now(timezone.utc).isoformat()}
    data['publications'].append(item); save_data(data); return item

@app.get('/api/publications/{publication_id}')
def get_publication(publication_id: str):
    item = next((p for p in data['publications'] if p['id']==publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    return item

@app.post('/api/publications/{publication_id}/like')
def like_publication(publication_id: str, user=Depends(current_user)):
    item = next((p for p in data['publications'] if p['id']==publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    item['likes'] += 1; save_data(data); return {'likes':item['likes']}

@app.post('/api/publications/{publication_id}/comments')
def comment_publication(publication_id: str, payload: CommentIn, user=Depends(current_user)):
    item = next((p for p in data['publications'] if p['id']==publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    comment={'id':secrets.token_hex(6),'text':payload.text,'author':user['name'],'created_at':datetime.now(timezone.utc).isoformat()}
    item['comments'].append(comment); save_data(data); return comment

@app.post('/api/ai/chat')
def ai_chat(message: str = Field(min_length=1), user=Depends(current_user)):
    return {'service':'Houmba H 1','status':'ready_gateway','message':'Le moteur IA est prêt à recevoir un fournisseur configuré.','received':message,'provider':settings.ai_provider or 'non configuré'}
