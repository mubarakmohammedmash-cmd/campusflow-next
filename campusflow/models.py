# campusflow/models.py
from campusflow.validation import validate_affected_users, validate_category, validate_title, validate_urgency

def calculate_priority(urgency: str, affected_users: int) -> str:
    """
    Preserve strict priority rule order:
    1. critical: high urgency AND affected_users >= 10
    2. high: high urgency OR affected_users >= 10
    3. medium: medium urgency OR affected_users >= 3
    4. low: otherwise
    """
    norm_urgency = urgency.strip().lower()
    
    if norm_urgency == "high" and affected_users >= 10:
        return "critical"
    elif norm_urgency == "high" or affected_users >= 10:
        return "high"
    elif norm_urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"

def create_ticket(ticket_id: str, title: str, category: str, urgency: str, affected_users: int, assigned_to: str = "") -> dict:
    """Create a new validated ticket dictionary with an empty notes list."""
    clean_title = validate_title(title)
    clean_cat = validate_category(category)
    clean_urg = validate_urgency(urgency)
    clean_users = validate_affected_users(affected_users)
    
    priority = calculate_priority(clean_urg, clean_users)
    
    return {
        "id": ticket_id,
        "title": clean_title,
        "category": clean_cat,
        "urgency": clean_urg,
        "affected_users": clean_users,
        "priority": priority,
        "status": "open",
        "assigned_to": assigned_to.strip(),
        "notes": []
    }
