#!/usr/bin/env python3
import os
import sys
import json
import time
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from auth.register import register_user, login_user, get_user_role
from tokens.generate import generate_token, validate_token
from messaging.send import send_message
from messaging.flag import flag_message
from rbac.access_control import check_permission
from logging.audit import log_event, get_events

def cleanup():
    """Clean up test data."""
    db_dir = Path(__file__).parent / 'db'
    logs_dir = Path(__file__).parent / 'logs'
    
    for file in db_dir.glob('*.json'):
        file.unlink()
    for file in logs_dir.glob('*.json'):
        file.unlink()

def test_registration():
    """Test user registration with Dartmouth emails."""
    print("\n=== Testing User Registration ===")
    
    # Test valid registration
    try:
        register_user("alice", "secret123", "Sender", "alice@dartmouth.edu")
        print("✅ Valid registration successful")
    except Exception as e:
        print(f"❌ Valid registration failed: {e}")
        return False
    
    # Test duplicate username
    try:
        register_user("alice", "secret123", "Sender", "alice2@dartmouth.edu")
        print("❌ Duplicate username should have failed")
        return False
    except ValueError as e:
        print("✅ Duplicate username correctly rejected")
    
    # Test non-Dartmouth email
    try:
        register_user("bob", "secret123", "Receiver", "bob@gmail.com")
        print("❌ Non-Dartmouth email should have failed")
        return False
    except ValueError as e:
        print("✅ Non-Dartmouth email correctly rejected")
    
    # Test duplicate email
    try:
        register_user("alice2", "secret123", "Sender", "alice@dartmouth.edu")
        print("❌ Duplicate email should have failed")
        return False
    except ValueError as e:
        print("✅ Duplicate email correctly rejected")
    
    return True

def test_login():
    """Test user login functionality."""
    print("\n=== Testing Login ===")
    
    # Test valid login
    if login_user("alice", "secret123"):
        print("✅ Valid login successful")
    else:
        print("❌ Valid login failed")
        return False
    
    # Test invalid password
    if not login_user("alice", "wrongpass"):
        print("✅ Invalid password correctly rejected")
    else:
        print("❌ Invalid password should have failed")
        return False
    
    # Test non-existent user
    if not login_user("nonexistent", "secret123"):
        print("✅ Non-existent user correctly rejected")
    else:
        print("❌ Non-existent user should have failed")
        return False
    
    return True

def test_tokens():
    """Test token generation and validation."""
    print("\n=== Testing Token System ===")
    
    # Test token generation
    try:
        token = generate_token("alice")
        print("✅ Token generation successful")
    except Exception as e:
        print(f"❌ Token generation failed: {e}")
        return False
    
    # Test token validation
    if validate_token(token) == "alice":
        print("✅ Token validation successful")
    else:
        print("❌ Token validation failed")
        return False
    
    # Test token reuse
    try:
        send_message("alice", token, "Test message")
        print("✅ Message sent with token")
    except Exception as e:
        print(f"❌ Message sending failed: {e}")
        return False
    
    # Test used token
    if validate_token(token) is None:
        print("✅ Used token correctly invalidated")
    else:
        print("❌ Used token should be invalid")
        return False
    
    return True

def test_rbac():
    """Test role-based access control."""
    print("\n=== Testing RBAC ===")
    
    # Register users with different roles
    try:
        register_user("receiver", "secret123", "Receiver", "receiver@dartmouth.edu")
        register_user("moderator", "secret123", "Moderator", "moderator@dartmouth.edu")
        print("✅ User registration for RBAC test successful")
    except Exception as e:
        print(f"❌ User registration for RBAC test failed: {e}")
        return False
    
    # Test Sender permissions
    if check_permission("alice", "get_token") and check_permission("alice", "send_message"):
        print("✅ Sender permissions correct")
    else:
        print("❌ Sender permissions incorrect")
        return False
    
    # Test Receiver permissions
    if check_permission("receiver", "view_messages") and not check_permission("receiver", "send_message"):
        print("✅ Receiver permissions correct")
    else:
        print("❌ Receiver permissions incorrect")
        return False
    
    # Test Moderator permissions
    if check_permission("moderator", "flag_message") and check_permission("moderator", "view_messages"):
        print("✅ Moderator permissions correct")
    else:
        print("❌ Moderator permissions incorrect")
        return False
    
    return True

def test_messaging():
    """Test messaging functionality."""
    print("\n=== Testing Messaging ===")
    
    # Generate new token for testing
    token = generate_token("alice")
    
    # Test message sending
    try:
        message_id = send_message("alice", token, "Test message")
        print("✅ Message sending successful")
    except Exception as e:
        print(f"❌ Message sending failed: {e}")
        return False
    
    # Test message flagging
    try:
        flag_id = flag_message("moderator", str(message_id))
        print("✅ Message flagging successful")
    except Exception as e:
        print(f"❌ Message flagging failed: {e}")
        return False
    
    return True

def test_audit_logging():
    """Test audit logging functionality."""
    print("\n=== Testing Audit Logging ===")
    
    # Test event logging
    try:
        log_event("test_event", {"test": "data"})
        print("✅ Event logging successful")
    except Exception as e:
        print(f"❌ Event logging failed: {e}")
        return False
    
    # Test event retrieval
    events = get_events(event_type="test_event")
    if events and events[0]["data"]["test"] == "data":
        print("✅ Event retrieval successful")
    else:
        print("❌ Event retrieval failed")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Starting WhisperChain+ Tests...")
    
    # Clean up any existing test data
    cleanup()
    
    # Run all tests
    tests = [
        ("Registration", test_registration),
        ("Login", test_login),
        ("Tokens", test_tokens),
        ("RBAC", test_rbac),
        ("Messaging", test_messaging),
        ("Audit Logging", test_audit_logging)
    ]
    
    all_passed = True
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} tests...")
        if not test_func():
            print(f"❌ {test_name} tests failed")
            all_passed = False
        else:
            print(f"✅ {test_name} tests passed")
    
    # Final cleanup
    cleanup()
    
    if all_passed:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 