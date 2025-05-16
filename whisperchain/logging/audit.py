import json
import time
from pathlib import Path

AUDIT_LOG = Path(__file__).parent.parent / 'db' / 'audit_log.json'

def _ensure_audit_log():
    """Ensure the audit log file exists."""
    AUDIT_LOG.parent.mkdir(exist_ok=True)
    if not AUDIT_LOG.exists():
        with open(AUDIT_LOG, 'w') as f:
            json.dump({
                'events': []
            }, f)

def log_event(event_type: str, data: dict) -> None:
    """
    Log an event to the audit log.
    Args:
        event_type: The type of event (e.g., 'registration', 'login', 'message_sent')
        data: Additional event data to log
    """
    _ensure_audit_log()
    
    # Load existing log
    with open(AUDIT_LOG, 'r') as f:
        log_data = json.load(f)
    
    # Create event entry
    event = {
        'timestamp': int(time.time()),
        'type': event_type,
        'data': data
    }
    
    # Add event to log
    log_data['events'].append(event)
    
    # Save updated log
    with open(AUDIT_LOG, 'w') as f:
        json.dump(log_data, f, indent=4)

def get_events(event_type: str = None, start_time: int = None, end_time: int = None) -> list:
    """
    Retrieve events from the audit log with optional filtering.
    
    Args:
        event_type: Filter events by type
        start_time: Filter events after this timestamp
        end_time: Filter events before this timestamp
    
    Returns:
        list: List of matching events
    """
    if not AUDIT_LOG.exists():
        return []
    
    with open(AUDIT_LOG, 'r') as f:
        log_data = json.load(f)
    
    events = log_data['events']
    
    # Apply filters
    if event_type:
        events = [e for e in events if e['type'] == event_type]
    if start_time:
        events = [e for e in events if e['timestamp'] >= start_time]
    if end_time:
        events = [e for e in events if e['timestamp'] <= end_time]
    
    return events 