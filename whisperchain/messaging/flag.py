import json
import time
from pathlib import Path

MESSAGES_DB = Path(__file__).parent.parent / 'db' / 'messages.json'
FLAGS_DB = Path(__file__).parent.parent / 'db' / 'flags.json'

def _ensure_flags_db():
    """Ensure the flags database file exists."""
    FLAGS_DB.parent.mkdir(exist_ok=True)
    if not FLAGS_DB.exists():
        with open(FLAGS_DB, 'w') as f:
            json.dump({
                'flags': {},
                'next_id': 1
            }, f)

def flag_message(username: str, message_id: str) -> int:
    """
    Flag a message for review.
    Args:
        username: The username of the moderator
        message_id: The ID of the message to flag
    Returns:
        int: The flag ID
    Raises:
        ValueError: If the message doesn't exist or is already flagged
    """
    _ensure_flags_db()
    
    # Check if message exists
    if not MESSAGES_DB.exists():
        raise ValueError("Messages database does not exist")
    
    with open(MESSAGES_DB, 'r') as f:
        messages_data = json.load(f)
    
    if message_id not in messages_data['messages']:
        raise ValueError("Message does not exist")
    
    message = messages_data['messages'][message_id]
    if message['flagged']:
        raise ValueError("Message is already flagged")
    
    # Load flags database
    with open(FLAGS_DB, 'r') as f:
        flags_data = json.load(f)
    
    # Generate flag ID
    flag_id = flags_data['next_id']
    flags_data['next_id'] += 1
    
    # Store flag
    timestamp = int(time.time())
    flags_data['flags'][str(flag_id)] = {
        'message_id': message_id,
        'moderator': username,
        'created_at': timestamp
    }
    
    # Mark message as flagged
    messages_data['messages'][message_id]['flagged'] = True
    
    # Save updated data
    with open(FLAGS_DB, 'w') as f:
        json.dump(flags_data, f, indent=4)
    
    with open(MESSAGES_DB, 'w') as f:
        json.dump(messages_data, f, indent=4)
    
    return flag_id 