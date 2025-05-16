from whisperchain.auth.register import register_user, login_user, get_user_role, DB_PATH
import json
from pathlib import Path

def clear_database():
    """Clear the users database."""
    if DB_PATH.exists():
        DB_PATH.unlink()
    DB_PATH.parent.mkdir(exist_ok=True)
    with open(DB_PATH, 'w') as f:
        json.dump({}, f)

def test_registration():
    print("\n=== Testing User Registration ===")
    
    # Clear the database first
    print("Clearing existing database...")
    clear_database()
    
    # Test 1: Valid Registration
    print("\nTest 1: Registering a valid user")
    try:
        register_user(
            username="alice",
            password="secret123",
            role="Sender",
            email="alice@dartmouth.edu"
        )
        print("✅ Registration successful!")
        
        # Verify login
        if login_user("alice", "secret123"):
            print("✅ Login successful!")
        else:
            print("❌ Login failed!")
            
        # Check role
        role = get_user_role("alice")
        print(f"✅ User role: {role}")
        
    except Exception as e:
        print(f"❌ Registration failed: {e}")
    
    # Test 2: Invalid Email
    print("\nTest 2: Registering with non-Dartmouth email")
    try:
        register_user(
            username="bob",
            password="secret123",
            role="Receiver",
            email="bob@gmail.com"
        )
        print("❌ Should have failed with non-Dartmouth email!")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")
    
    # Test 3: Invalid Role
    print("\nTest 3: Registering with invalid role")
    try:
        register_user(
            username="charlie",
            password="secret123",
            role="InvalidRole",
            email="charlie@dartmouth.edu"
        )
        print("❌ Should have failed with invalid role!")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")
    
    # Test 4: Duplicate Username
    print("\nTest 4: Registering with duplicate username")
    try:
        register_user(
            username="alice",  # Same as first test
            password="secret456",
            role="Receiver",
            email="alice2@dartmouth.edu"
        )
        print("❌ Should have failed with duplicate username!")
    except ValueError as e:
        print(f"✅ Correctly caught error: {e}")

if __name__ == "__main__":
    test_registration() 