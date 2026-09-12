from datetime import datetime, timedelta, timezone
from hashlib import sha256
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = sha256(f"{salt}:{password}".encode()).hexdigest()
    return f"{salt}${digest}"


def verify_password(password: str, stored: str) -> bool:
    try:
        salt, digest = stored.split("$", 1)
    except ValueError:
        return False
    return sha256(f"{salt}:{password}".encode()).hexdigest() == digest


def expires_at(hours: int = 24) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=hours)).isoformat()
