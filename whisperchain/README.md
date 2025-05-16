# WhisperChain+

A secure, anonymous messaging system with role-based access control.

## Features

- User Registration System with role-based access (Sender, Receiver, Moderator)
- Dartmouth-only access (requires @dartmouth.edu email)
- Anonymous Token Generation for secure message sending
- Role-Based Access Control (RBAC)
- Comprehensive Audit Logging
- Command-Line Interface

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/whisperchain.git
cd whisperchain
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

The application provides the following commands:

### User Management
```bash
# Register a new user (requires Dartmouth email)
python cli.py register --username alice --password secret123 --role Sender --email alice@dartmouth.edu

# Login
python cli.py login --username alice --password secret123
```

### Messaging
```bash
# Get an anonymous token (Sender only)
python cli.py get-token --username alice --password secret123

# Send a message (Sender only)
python cli.py send --username alice --password secret123 --token "your-token-here" --message "Hello, world!"

# View messages (Receiver only)
python cli.py view --username bob --password secret123

# Flag a message (Moderator only)
python cli.py flag --username moderator --password secret123 --message-id 1
```

## Security Features

- Dartmouth-only access with email verification
- Passwords are hashed using SHA-256 with unique salts
- Anonymous tokens are single-use and cryptographically secure
- Role-based access control for all operations
- Comprehensive audit logging of all system events

## Data Storage

All data is stored in JSON files:
- `db/users.json`: User credentials, roles, and Dartmouth emails
- `db/tokens.json`: Anonymous tokens
- `db/messages.json`: Messages
- `db/flags.json`: Flagged messages
- `logs/audit_log.json`: System audit log

## License

MIT License 