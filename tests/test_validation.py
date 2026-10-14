# tests/test_validation.py
import unittest
from campusflow.validation import validate_affected_users, validate_category, validate_title

class TestValidation(unittest.TestCase):
    def test_valid_affected_users(self):
        self.assertEqual(validate_affected_users(5), 5)
        self.assertEqual(validate_affected_users(1), 1)

    def test_invalid_affected_users_type(self):
        with self.assertRaises(TypeError):
            validate_affected_users(True)
        with self.assertRaises(TypeError):
            validate_affected_users("10")
            
    def test_invalid_affected_users_range(self):
        with self.assertRaises(ValueError):
            validate_affected_users(0)
        with self.assertRaises(ValueError):
            validate_affected_users(-3)

    def test_valid_category(self):
        self.assertEqual(validate_category("network"), "Network")

    def test_invalid_category(self):
        with self.assertRaises(ValueError):
            validate_category("Power")

if __name__ == "__main__":
    unittest.main()
