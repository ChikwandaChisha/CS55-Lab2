import unittest
from whisperchain.messaging.send import send_message
from whisperchain.messaging.flag import flag_message
from whisperchain.auth.register import register_user
from whisperchain.tokens.generate import generate_token

class TestMessaging(unittest.TestCase):
    def setUp(self):
        # Register test users
        try:
            register_user("sender_msg", "password123", "Sender", "sender_msg@dartmouth.edu")
            register_user("moderator_msg", "password123", "Moderator", "moderator_msg@dartmouth.edu")
        except ValueError:
            pass  # Users might already exist

    def test_send_message(self):
        # Generate a token for the sender
        token = generate_token("sender_msg")
        
        # Test sending a message
        message_id = send_message("sender_msg", token, "Test message")
        self.assertIsNotNone(message_id)
        
        # Test sending with invalid token
        with self.assertRaises(ValueError):
            send_message("sender_msg", "invalid_token", "Test message")
        
        # Test sending with used token
        with self.assertRaises(ValueError):
            send_message("sender_msg", token, "Test message")

    def test_flag_message(self):
        # Generate a token and send a message
        token = generate_token("sender_msg")
        message_id = send_message("sender_msg", token, "Test message for flagging")
        
        # Test flagging a message
        flag_id = flag_message("moderator_msg", str(message_id))
        self.assertIsNotNone(flag_id)
        
        # Test flagging non-existent message
        with self.assertRaises(ValueError):
            flag_message("moderator_msg", "999999")
        
        # Test flagging with non-moderator
        with self.assertRaises(ValueError):
            flag_message("sender_msg", str(message_id))

if __name__ == "__main__":
    unittest.main() 