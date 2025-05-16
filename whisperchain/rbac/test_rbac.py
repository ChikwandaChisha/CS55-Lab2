import unittest
from whisperchain.rbac.access_control import check_permission
from whisperchain.auth.register import register_user

class TestRBAC(unittest.TestCase):
    def setUp(self):
        # Register test users with different roles
        try:
            register_user("sender_test", "password123", "Sender", "sender_test@dartmouth.edu")
            register_user("receiver_test", "password123", "Receiver", "receiver_test@dartmouth.edu")
            register_user("moderator_test", "password123", "Moderator", "moderator_test@dartmouth.edu")
        except ValueError:
            pass  # Users might already exist

    def test_sender_permissions(self):
        # Test Sender permissions
        self.assertTrue(check_permission("sender_test", "get_token"))
        self.assertTrue(check_permission("sender_test", "send_message"))
        self.assertFalse(check_permission("sender_test", "view_messages"))
        self.assertFalse(check_permission("sender_test", "flag_message"))

    def test_receiver_permissions(self):
        # Test Receiver permissions
        self.assertFalse(check_permission("receiver_test", "get_token"))
        self.assertFalse(check_permission("receiver_test", "send_message"))
        self.assertTrue(check_permission("receiver_test", "view_messages"))
        self.assertFalse(check_permission("receiver_test", "flag_message"))

    def test_moderator_permissions(self):
        # Test Moderator permissions
        self.assertFalse(check_permission("moderator_test", "get_token"))
        self.assertFalse(check_permission("moderator_test", "send_message"))
        self.assertTrue(check_permission("moderator_test", "view_messages"))
        self.assertTrue(check_permission("moderator_test", "flag_message"))

if __name__ == "__main__":
    unittest.main() 