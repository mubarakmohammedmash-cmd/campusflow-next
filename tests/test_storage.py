# tests/test_storage.py
import unittest
import os
import json
from campusflow.models import create_ticket
from campusflow.storage import save_tickets, load_tickets, get_next_ticket_id

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.test_file = "test_tickets.json"

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_save_and_load_tickets(self):
        ticket = create_ticket("T001", "Wi-Fi Issue", "Network", "high", 10, "Staff A")
        save_tickets(self.test_file, [ticket])
        
        loaded = load_tickets(self.test_file)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0]["id"], "T001")
        self.assertEqual(loaded[0]["priority"], "critical")

    def test_duplicate_id_rejection(self):
        data = {
            "tickets": [
                {"id": "T001", "title": "Test 1", "category": "Network", "urgency": "low", "affected_users": 1, "status": "open", "notes": []},
                {"id": "T001", "title": "Test 2", "category": "Hardware", "urgency": "low", "affected_users": 1, "status": "open", "notes": []}
            ]
        }
        with open(self.test_file, "w") as f:
            json.dump(data, f)
            
        with self.assertRaises(ValueError):
            load_tickets(self.test_file)

    def test_next_ticket_id(self):
        tickets = [{"id": "T001"}, {"id": "T005"}]
        self.assertEqual(get_next_ticket_id(tickets), "T006")

if __name__ == "__main__":
    unittest.main()
