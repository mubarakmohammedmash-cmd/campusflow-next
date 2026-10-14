# tests/test_notes.py
import unittest
from campusflow.models import create_ticket, calculate_priority
from campusflow.notes import add_note_to_ticket

class TestNotesAndPriority(unittest.TestCase):
    def test_priority_rules(self):
        self.assertEqual(calculate_priority("high", 12), "critical")
        self.assertEqual(calculate_priority("high", 5), "high")
        self.assertEqual(calculate_priority("medium", 3), "medium")
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_add_note_success(self):
        ticket = create_ticket("T001", "Wi-Fi down", "Network", "high", 5, "Staff A")
        note = add_note_to_ticket(ticket, "Mentor A", "Rebooted router successfully.")
        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(len(ticket["notes"]), 1)

    def test_add_note_rejected_on_resolved(self):
        ticket = create_ticket("T002", "Printer error", "Hardware", "low", 1, "Staff B")
        ticket["status"] = "resolved"
        with self.assertRaises(ValueError):
            add_note_to_ticket(ticket, "Mentor A", "Trying to fix printer.")
        self.assertEqual(len(ticket["notes"]), 0)

    def test_invalid_note_message_length(self):
        ticket = create_ticket("T003", "Software crash", "Software", "medium", 2)
        with self.assertRaises(ValueError):
            add_note_to_ticket(ticket, "Mentor B", "Hi")  # Too short (< 5 chars)

if __name__ == "__main__":
    unittest.main()
