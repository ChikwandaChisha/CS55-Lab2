import json
import time
from pathlib import Path
from tokens.generate import validate_token, mark_token_used

MESSAGES_DB = Path(__file__).parent.parent / 'db' / 'messages.json'
RECEIVERS_DB = Path(__file__).parent.parent / 'db' / 'receivers.json'

def _ensure_messages_db():
    """Ensure the messages database file exists."""
    MESSAGES_DB.parent.mkdir(exist_ok=True)
    if not MESSAGES_DB.exists():
        with open(MESSAGES_DB, 'w') as f:
            json.dump({
                'messages': {},
                'next_id': 1
            }, f)

def _ensure_receivers_db():
    """Ensure the receivers database file exists."""
    RECEIVERS_DB.parent.mkdir(exist_ok=True)
    if not RECEIVERS_DB.exists():
        with open(RECEIVERS_DB, 'w') as f:
            json.dump({
                'receivers': {}
            }, f)

def send_message(username: str, token: str, message: str, receiver: str) -> int:
    """
    Send a message using an anonymous token to a specific receiver.
    Args:
        username: The username of the sender
        token: The anonymous token to use
        message: The message content
        receiver: The username of the receiver
    Returns:
        int: The message ID
    Raises:
        ValueError: If the token is invalid or already used, or receiver does not exist
    """
    _ensure_messages_db()
    _ensure_receivers_db()
    
    # Validate token
    token_username = validate_token(token)
    if not token_username or token_username != username:
        raise ValueError("Invalid or already used token")
    
    # Load messages database
    with open(MESSAGES_DB, 'r') as f:
        data = json.load(f)
    
    # Generate message ID
    message_id = data['next_id']
    data['next_id'] += 1
    
    # Store message
    timestamp = int(time.time())
    data['messages'][str(message_id)] = {
        'content': message,
        'token': token,
        'created_at': timestamp,
        'flagged': False,
        'read_by': []
    }
    
    # Mark token as used
    mark_token_used(token)
    
    # Save updated messages
    with open(MESSAGES_DB, 'w') as f:
        json.dump(data, f, indent=4)
    
    # Add message to the specified receiver's queue
    with open(RECEIVERS_DB, 'r') as f:
        receivers_data = json.load(f)
    
    if receiver not in receivers_data['receivers']:
        raise ValueError(f"Receiver '{receiver}' does not exist.")
    
    if 'messages' not in receivers_data['receivers'][receiver]:
        receivers_data['receivers'][receiver]['messages'] = []
    receivers_data['receivers'][receiver]['messages'].append({
        'message_id': str(message_id),
        'received_at': timestamp,
        'read': False
    })
    
    # Save updated receivers data
    with open(RECEIVERS_DB, 'w') as f:
        json.dump(receivers_data, f, indent=4)
    
    return message_id

def get_receiver_messages(username: str) -> list:
    """
    Get all messages for a receiver.
    Args:
        username: The username of the receiver
    Returns:
        list: List of messages with their read status
    """
    if not RECEIVERS_DB.exists() or not MESSAGES_DB.exists():
        return []
    
    with open(RECEIVERS_DB, 'r') as f:
        receivers_data = json.load(f)
    
    if username not in receivers_data['receivers']:
        return []
    
    receiver_messages = receivers_data['receivers'][username].get('messages', [])
    
    # Load message contents
    with open(MESSAGES_DB, 'r') as f:
        messages_data = json.load(f)
    
    # Combine message content with receiver's read status
    result = []
    for msg in receiver_messages:
        message_id = msg['message_id']
        if message_id in messages_data['messages']:
            message_content = messages_data['messages'][message_id]
            result.append({
                'message_id': message_id,
                'content': message_content['content'],
                'created_at': message_content['created_at'],
                'received_at': msg['received_at'],
                'read': msg['read'],
                'flagged': message_content['flagged']
            })
    
    return result

def mark_message_read(username: str, message_id: str) -> None:
    """
    Mark a message as read by a receiver.
    Args:
        username: The username of the receiver
        message_id: The ID of the message to mark as read
    """
    if not RECEIVERS_DB.exists():
        return
    
    with open(RECEIVERS_DB, 'r') as f:
        receivers_data = json.load(f)
    
    if username not in receivers_data['receivers']:
        return
    
    # Find and mark the message as read
    for msg in receivers_data['receivers'][username].get('messages', []):
        if msg['message_id'] == message_id:
            msg['read'] = True
            break
    
    # Save updated data
    with open(RECEIVERS_DB, 'w') as f:
        json.dump(receivers_data, f, indent=4) 