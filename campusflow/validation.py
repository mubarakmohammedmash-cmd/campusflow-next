# campusflow/validation.py

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}
VALID_URGENCIES = {"low", "medium", "high"}
VALID_STATUSES = {"open", "in_progress", "resolved"}

def validate_category(category: str) -> str:
    """Normalize and validate ticket category."""
    if not isinstance(category, str):
        raise TypeError("Category must be a string.")
    normalized = category.strip().capitalize()
    if normalized not in VALID_CATEGORIES:
        raise ValueError(f"Invalid category '{category}'. Must be one of {list(VALID_CATEGORIES)}.")
    return normalized

def validate_urgency(urgency: str) -> str:
    """Normalize and validate ticket urgency."""
    if not isinstance(urgency, str):
        raise TypeError("Urgency must be a string.")
    normalized = urgency.strip().lower()
    if normalized not in VALID_URGENCIES:
        raise ValueError(f"Invalid urgency '{urgency}'. Must be one of {list(VALID_URGENCIES)}.")
    return normalized

def validate_affected_users(affected_users) -> int:
    """
    Validate affected_users must be a strictly positive integer.
    Rejects floats, strings, and booleans masquerading as ints.
    """
    if isinstance(affected_users, bool) or not isinstance(affected_users, (int, float)):
        raise TypeError("Affected users must be an integer.")
    if isinstance(affected_users, float) and not affected_users.is_integer():
        raise ValueError("Affected users cannot be a float.")
    
    val = int(affected_users)
    if val <= 0:
        raise ValueError("Affected users must be a strictly positive integer greater than 0.")
    return val

def validate_title(title: str) -> str:
    """Validate title is not blank after trimming."""
    if not isinstance(title, str):
        raise TypeError("Title must be a string.")
    cleaned = title.strip()
    if not cleaned:
        raise ValueError("Title cannot be blank.")
    return cleaned
