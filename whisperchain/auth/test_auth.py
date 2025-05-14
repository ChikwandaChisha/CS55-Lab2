import unittest
from whisperchain.auth.register import register_user, login_user, get_user_role

class TestAuth(unittest.TestCase):
    def setUp(self):
        # Clean up any existing test users
        pass

    def test_register_user(self):
        # Test valid registration
        register_user("testuser1", "password123", "Sender", "test1@dartmouth.edu")
        self.assertEqual(get_user_role("testuser1"), "Sender")

        # Test duplicate username
        with self.assertRaises(ValueError):
            register_user("testuser1", "password123", "Sender", "test2@dartmouth.edu")

        # Test non-Dartmouth email
        with self.assertRaises(ValueError):
            register_user("testuser2", "password123", "Sender", "test@gmail.com")

        # Test duplicate email
        with self.assertRaises(ValueError):
            register_user("testuser3", "password123", "Sender", "test1@dartmouth.edu")

    def test_login_user(self):
        # Register a test user
        register_user("testuser4", "password123", "Receiver", "test4@dartmouth.edu")

        # Test valid login
        self.assertTrue(login_user("testuser4", "password123"))

        # Test invalid password
        self.assertFalse(login_user("testuser4", "wrongpassword"))

        # Test non-existent user
        self.assertFalse(login_user("nonexistent", "password123"))

    def test_get_user_role(self):
        # Register users with different roles
        register_user("sender1", "password123", "Sender", "sender1@dartmouth.edu")
        register_user("receiver1", "password123", "Receiver", "receiver1@dartmouth.edu")
        register_user("moderator1", "password123", "Moderator", "moderator1@dartmouth.edu")

        # Test role retrieval
        self.assertEqual(get_user_role("sender1"), "Sender")
        self.assertEqual(get_user_role("receiver1"), "Receiver")
        self.assertEqual(get_user_role("moderator1"), "Moderator")

        # Test non-existent user
        self.assertIsNone(get_user_role("nonexistent"))

if __name__ == "__main__":
    unittest.main() 