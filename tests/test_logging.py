import unittest
import time
import json
from pathlib import Path
from whisperchain.logging.audit import log_event, get_events, AUDIT_LOG

class TestAuditLogging(unittest.TestCase):
    def setUp(self):
        # Clear the audit log before each test
        if AUDIT_LOG.exists():
            AUDIT_LOG.unlink()
    
    def test_log_event_creates_file(self):
        """Test that logging an event creates the audit log file"""
        log_event('test_event', {'message': 'test'})
        self.assertTrue(AUDIT_LOG.exists())
        
        with open(AUDIT_LOG, 'r') as f:
            data = json.load(f)
            self.assertIn('events', data)
            self.assertEqual(len(data['events']), 1)
            self.assertEqual(data['events'][0]['type'], 'test_event')
    
    def test_get_events_filtering(self):
        """Test retrieving events with different filters"""
        # Log multiple events and record timestamps
        log_event('type1', {'data': 'first'})
        ts1 = int(time.time())
        time.sleep(1)
        log_event('type2', {'data': 'second'})
        ts2 = int(time.time())
        time.sleep(1)
        log_event('type1', {'data': 'third'})
        ts3 = int(time.time())
        
        # Test type filtering
        type1_events = get_events(event_type='type1')
        self.assertEqual(len(type1_events), 2)
        
        # Test time filtering: only the last event
        recent_events = get_events(start_time=ts3)
        self.assertEqual(len(recent_events), 1)
        self.assertEqual(recent_events[0]['data']['data'], 'third')
        
        # Test combined filtering: only the second event
        filtered_events = get_events(
            event_type='type2',
            start_time=ts2,
            end_time=ts2
        )
        self.assertEqual(len(filtered_events), 1)
        self.assertEqual(filtered_events[0]['data']['data'], 'second')
    
    def test_empty_log_returns_empty_list(self):
        """Test that get_events returns empty list when log doesn't exist"""
        events = get_events()
        self.assertEqual(events, [])

if __name__ == '__main__':
    unittest.main() 