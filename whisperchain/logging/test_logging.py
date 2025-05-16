import unittest
from whisperchain.logging.audit import log_event, get_events
import time

class TestLogging(unittest.TestCase):
    def setUp(self):
        # Clean up any existing test logs
        pass

    def test_log_event(self):
        # Test logging a simple event
        event_data = {"action": "test", "user": "testuser"}
        log_event("test_event", event_data)
        
        # Verify the event was logged
        events = get_events(event_type="test_event")
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["data"], event_data)
        
        # Test logging multiple events
        log_event("test_event", {"action": "test2", "user": "testuser"})
        events = get_events(event_type="test_event")
        self.assertEqual(len(events), 2)

    def test_get_events(self):
        # Log some test events
        log_event("test_event1", {"data": "test1"})
        log_event("test_event2", {"data": "test2"})
        log_event("test_event1", {"data": "test3"})
        
        # Test getting events by type
        events1 = get_events(event_type="test_event1")
        self.assertEqual(len(events1), 2)
        
        events2 = get_events(event_type="test_event2")
        self.assertEqual(len(events2), 1)
        
        # Test getting non-existent event type
        events3 = get_events(event_type="nonexistent")
        self.assertEqual(len(events3), 0)
        
        # Test event ordering (most recent first)
        self.assertEqual(events1[0]["data"]["data"], "test3")
        self.assertEqual(events1[1]["data"]["data"], "test1")

if __name__ == "__main__":
    unittest.main() 