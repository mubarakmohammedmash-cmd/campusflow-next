# tests/test_search.py
import unittest
from campusflow.models import create_ticket
from campusflow.search import search_tickets

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            create_ticket("T001", "Wi-Fi router down", "Network", "high", 12),
            create_ticket("T002", "Printer jammed", "Hardware", "low", 1),
            create_ticket("T003", "Wi-Fi password reset", "Network", "medium", 2),
        ]

    def test_case_insensitive_substring_search(self):
        results = search_tickets(self.tickets, query="WI-FI")
        self.assertEqual(len(results), 2)

    def test_combined_filters_and(self):
        # Query matches "Wi-Fi" (case-insensitive substring)
        results = search_tickets(self.tickets, query="Wi-Fi", category="Network", urgency="high")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["id"], "T001")

if __name__ == "__main__":
    unittest.main()
