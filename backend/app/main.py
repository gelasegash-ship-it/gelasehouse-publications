"""API HOUMBA H : publications, authentification, interactions et passerelle IA."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib, hmac, json, secrets
from typing import Optional

from fastapi import FastAPI, HTTPException, Header, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from .config import get_settings

settings = get_settings()
app = FastAPI(title="Houmba H API", version="1.1.0", description="Backend de HOUMBA H et de Houmba H 1")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(',') if x.strip()], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])

DATA_FILE = Path(__file__).resolve().parent.parent / "houmba_data.json"

def load_data():
    if not DATA_FILE.exists():
        return {"users": [], "publications": [], "tokens": {}, "likes": {}}
    try:
        value = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        value.setdefault("users", []); value.setdefault("publications", []); value.setdefault("tokens", {}); value.setdefault("likes", {})
        return value
    except (OSError, json.JSONDecodeError):
        return {"users": [], "publications": [], "tokens": {}, "likes": {}}

def save_data(value):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary = DATA_FILE.with_suffix('.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(DATA_FILE)

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

class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=10000)

def password_hash(password: str, salt: str | None = None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 120000).hex()
    return f"{salt}${digest}"

def password_ok(password, stored):
    try:
        salt, digest = stored.split('$', 1)
        return hmac.compare_digest(password_hash(password, salt).split('$', 1)[1], digest)
    except ValueError:
        return False

def current_user(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith('Bearer '):
        raise HTTPException(401, 'Authentification requise')
    user_id = data['tokens'].get(authorization[7:])
    user = next((u for u in data['users'] if u['id'] == user_id), None)
    if not user:
        raise HTTPException(401, 'Session invalide')
    return user

def public_user(user):
    return {'id': user['id'], 'name': user['name'], 'email': user['email']}

def now():
    return datetime.now(timezone.utc).isoformat()

@app.get('/health')
def health():
    return {'status': 'ok', 'service': 'houmba-h-api', 'version': '1.1.0', 'timestamp': now()}

@app.post('/api/auth/register', status_code=201)
def register(payload: RegisterIn):
    if any(u['email'].lower() == payload.email.lower() for u in data['users']):
        raise HTTPException(409, 'Cet email existe déjà')
    user = {'id': secrets.token_hex(8), 'name': payload.name.strip(), 'email': payload.email.lower(), 'password_hash': password_hash(payload.password), 'created_at': now()}
    data['users'].append(user); save_data(data)
    return public_user(user)

@app.post('/api/auth/login')
def login(payload: LoginIn):
    user = next((u for u in data['users'] if u['email'] == payload.email.lower()), None)
    if not user or not password_ok(payload.password, user['password_hash']):
        raise HTTPException(401, 'Email ou mot de passe incorrect')
    token = secrets.token_urlsafe(32); data['tokens'][token] = user['id']; save_data(data)
    return {'access_token': token, 'token_type': 'bearer', 'user': public_user(user)}

@app.post('/api/auth/logout')
def logout(authorization: Optional[str] = Header(default=None)):
    if authorization and authorization.startswith('Bearer '):
        data['tokens'].pop(authorization[7:], None); save_data(data)
    return {'status': 'ok'}

@app.get('/api/me')
def me(user=Depends(current_user)):
    return {**public_user(user), 'created_at': user['created_at']}

@app.get('/api/publications')
def list_publications(q: Optional[str] = Query(default=None, max_length=200), category: Optional[str] = Query(default=None, max_length=80)):
    items = list(reversed(data['publications']))
    if q:
        needle = q.lower().strip(); items = [p for p in items if needle in (p['title'] + ' ' + p['description'] + ' ' + p['author']['name']).lower()]
    if category:
        items = [p for p in items if p['category'].lower() == category.lower()]
    return items

@app.post('/api/publications', status_code=201)
def create_publication(payload: PublicationIn, user=Depends(current_user)):
    item = {'id': secrets.token_hex(8), 'title': payload.title.strip(), 'description': payload.description.strip(), 'category': payload.category.strip() or 'Général', 'cover_url': payload.cover_url, 'author': {'id': user['id'], 'name': user['name']}, 'likes': 0, 'comments': [], 'created_at': now()}
    data['publications'].append(item); save_data(data); return item

@app.get('/api/publications/{publication_id}')
def get_publication(publication_id: str):
    item = next((p for p in data['publications'] if p['id'] == publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    return item

@app.post('/api/publications/{publication_id}/like')
def like_publication(publication_id: str, user=Depends(current_user)):
    item = next((p for p in data['publications'] if p['id'] == publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    liked_by = data['likes'].setdefault(publication_id, [])
    if user['id'] not in liked_by:
        liked_by.append(user['id']); item['likes'] = len(liked_by); save_data(data)
    return {'likes': item['likes'], 'liked': True}

@app.post('/api/publications/{publication_id}/comments')
def comment_publication(publication_id: str, payload: CommentIn, user=Depends(current_user)):
    item = next((p for p in data['publications'] if p['id'] == publication_id), None)
    if not item: raise HTTPException(404, 'Publication introuvable')
    comment = {'id': secrets.token_hex(6), 'text': payload.text.strip(), 'author': user['name'], 'created_at': now()}
    item.setdefault('comments', []).append(comment); save_data(data); return comment

@app.post('/api/ai/chat')
def ai_chat(payload: ChatIn, user=Depends(current_user)):
    return {'service': 'Houmba H 1', 'status': 'ready_gateway', 'message': 'Le moteur IA est prêt. Configurez AI_PROVIDER, AI_API_KEY et AI_MODEL pour activer un fournisseur.', 'received': payload.message, 'provider': settings.ai_provider or 'non configuré'}
