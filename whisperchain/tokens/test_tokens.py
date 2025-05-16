import unittest
from whisperchain.tokens.generate import generate_token, validate_token
from whisperchain.auth.register import register_user

class TestTokens(unittest.TestCase):
    def setUp(self):
        # Register a test user before each test
        try:
            register_user("testuser", "password123", "Sender", "test@dartmouth.edu")
        except ValueError:
            pass  # User might already exist

    def test_generate_token(self):
        # Test token generation for valid user
        token = generate_token("testuser")
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 32)  # Assuming tokens are 32 characters

        # Test token generation for invalid user
        with self.assertRaises(ValueError):
            generate_token("nonexistentuser")

    def test_validate_token(self):
        # Generate a token
        token = generate_token("testuser")
        
        # Test valid token
        username = validate_token(token)
        self.assertEqual(username, "testuser")
        
        # Test invalid token
        invalid_token = "invalid" * 4  # 32 characters but invalid
        self.assertIsNone(validate_token(invalid_token))

    def test_token_single_use(self):
        # Generate a token
        token = generate_token("testuser")
        
        # First use should be valid
        username = validate_token(token)
        self.assertEqual(username, "testuser")
        
        # Second use should be invalid
        self.assertIsNone(validate_token(token))

if __name__ == "__main__":
    unittest.main() 