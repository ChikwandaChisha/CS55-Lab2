import json
import os
import hashlib
import secrets
import re
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / 'db' / 'users.json'

def _ensure_db_exists():
    """Ensure the users database file exists."""
    DB_PATH.parent.mkdir(exist_ok=True)
    if not DB_PATH.exists():
        with open(DB_PATH, 'w') as f:
            json.dump({}, f)

def _hash_password(password: str, salt: str = None) -> tuple[str, str]:
    """Hash a password with a salt."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return hashed, salt

def _validate_dartmouth_email(email: str) -> bool:
    # Validate that the email is a Dartmouth email address.
    dartmouth_pattern = r'^[a-zA-Z0-9._%+-]+@dartmouth\.edu$'
    return bool(re.match(dartmouth_pattern, email))

def register_user(username: str, password: str, role: str, email: str) -> None:
    """
    Register a new user with the given credentials and role.
    Args:
        username: The username for the account
        password: The user's password
        role: The user's role (Sender, Receiver, or Moderator)
        email: The user's Dartmouth email address
    Raises:
        ValueError: If the email is not a valid Dartmouth email or if other validations fail
    """
    _ensure_db_exists()
    
    # Validate email
    if not _validate_dartmouth_email(email):
        raise ValueError("Only Dartmouth email addresses (@dartmouth.edu) are allowed")
    
    # Validate role
    if role.lower() not in ['sender', 'receiver', 'moderator', 'admin']:
        raise ValueError("Invalid role. Must be one of: Sender, Receiver, Moderator, Admin")
    
    # Load existing users
    with open(DB_PATH, 'r') as f:
        users = json.load(f)
    
    # Check if username already exists
    if username in users:
        raise ValueError("Username already exists")
    
    # Check if email already registered
    for user_data in users.values():
        if user_data.get('email') == email:
            raise ValueError("Email address already registered")
    
    # Hash password and store user
    hashed_password, salt = _hash_password(password)
    users[username] = {
        'password_hash': hashed_password,
        'salt': salt,
        'role': role,
        'email': email
    }
    
    # Save updated users
    with open(DB_PATH, 'w') as f:
        json.dump(users, f, indent=4)

def login_user(username: str, password: str) -> bool:
    """Verify user credentials and return True if valid."""
    if not DB_PATH.exists():
        return False
    
    with open(DB_PATH, 'r') as f:
        users = json.load(f)
    
    if username not in users:
        return False
    
    user = users[username]
    hashed_password, _ = _hash_password(password, user['salt'])
    return hashed_password == user['password_hash']

def get_user_role(username: str) -> str:
    # Get the role of a user.
    if not DB_PATH.exists():
        raise ValueError("User database does not exist")
    
    with open(DB_PATH, 'r') as f:
        users = json.load(f)
    
    if username not in users:
        raise ValueError("User does not exist")
    
    return users[username]['role'] 
