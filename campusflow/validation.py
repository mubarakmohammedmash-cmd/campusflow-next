"""Validation helpers.

Contract: each function returns the cleaned value if the input is valid,
and raises ValueError if it is not. None of them change any data.
"""

CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}
URGENCIES = ("low", "medium", "high")
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("low", "medium", "high", "critical")


def validate_title(title):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title cannot be blank.")
    return title.strip()


def validate_category(category):
    key = category.strip().casefold() if isinstance(category, str) else None
    if key not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software or Other.")
    return CATEGORIES[key]


def validate_urgency(urgency):
    value = urgency.strip().casefold() if isinstance(urgency, str) else None
    if value not in URGENCIES:
        raise ValueError("Urgency must be low, medium or high.")
    return value


def validate_affected_users(value):
    # bool is a subclass of int in Python, so True would pass isinstance(True, int).
    # We must reject it explicitly.
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError("Affected users must be a whole number of 1 or more.")
    return value


def validate_staff(staff):
    if not isinstance(staff, str) or not staff.strip():
        raise ValueError("Staff label cannot be blank.")
    return staff.strip()
