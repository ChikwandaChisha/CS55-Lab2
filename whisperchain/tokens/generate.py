import json
import secrets
import time
from pathlib import Path
from typing import Optional

TOKENS_DB = Path(__file__).parent.parent / 'db' / 'tokens.json'

def _ensure_tokens_db():
    """Ensure the tokens database file exists."""
    TOKENS_DB.parent.mkdir(exist_ok=True)
    if not TOKENS_DB.exists():
        with open(TOKENS_DB, 'w') as f:
            json.dump({
                'tokens': {},
                'issued': {}
            }, f)

def generate_token(username: str) -> str:
    """Generate a new anonymous token for a user."""
    _ensure_tokens_db()
    
    # Load existing tokens
    with open(TOKENS_DB, 'r') as f:
        data = json.load(f)
    
    # Check if user already has an unused token
    for token, info in data['tokens'].items():
        if info['username'] == username and not info['used']:
            return token
    
    # Generate new token
    token = secrets.token_urlsafe(32)
    timestamp = int(time.time())
    
    # Store token
    data['tokens'][token] = {
        'username': username,
        'created_at': timestamp,
        'used': False
    }
    
    # Log issuance
    data['issued'][timestamp] = {
        'username': username,
        'token': token
    }
    
    # Save updated data
    with open(TOKENS_DB, 'w') as f:
        json.dump(data, f, indent=4)
    
    return token

def validate_token(token: str) -> Optional[str]:
    """Validate a token and return the associated username if valid."""
    if not TOKENS_DB.exists():
        return None
    
    with open(TOKENS_DB, 'r') as f:
        data = json.load(f)
    
    if token not in data['tokens']:
        return None
    
    token_info = data['tokens'][token]
    if token_info['used']:
        return None
    
    return token_info['username']

def mark_token_used(token: str) -> None:
    """Mark a token as used."""
    if not TOKENS_DB.exists():
        raise ValueError("Tokens database does not exist")
    
    with open(TOKENS_DB, 'r') as f:
        data = json.load(f)
    
    if token not in data['tokens']:
        raise ValueError("Invalid token")
    
    data['tokens'][token]['used'] = True
    
    with open(TOKENS_DB, 'w') as f:
        json.dump(data, f, indent=4) 