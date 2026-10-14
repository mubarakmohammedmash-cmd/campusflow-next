# campusflow/storage.py
import json
import os
from campusflow.models import create_ticket

def save_tickets(filepath: str, tickets: list) -> None:
    """Save the full collection of tickets (including notes) to JSON safely."""
    data = {
        "tickets": tickets
    }
    # Write atomically or directly
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_tickets(filepath: str) -> list:
    """
    Load and validate the full ticket collection from JSON.
    If the file doesn't exist, return an empty list.
    If any record is invalid or duplicate IDs exist, raise ValueError 
    and refuse to return partial/corrupted data.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in storage file: {e}")

    if isinstance(data, list):
        # Support legacy list format if needed
        raw_tickets = data
    elif isinstance(data, dict) and "tickets" in data:
        raw_tickets = data["tickets"]
    else:
        raise ValueError("Invalid storage structure: root must be a list or a dict with a 'tickets' key.")

    validated_tickets = []
    seen_ids = set()

    for item in raw_tickets:
        if not isinstance(item, dict):
            raise ValueError("Each ticket record must be a dictionary.")
        
        t_id = item.get("id")
        if not t_id or not isinstance(t_id, str):
            raise ValueError("Every ticket must have a valid string ID.")
        
        if t_id in seen_ids:
            raise ValueError(f"Duplicate ticket ID found: '{t_id}'. Load rejected.")
        seen_ids.add(t_id)

        # Validate core fields through model creation helper
        try:
            ticket = create_ticket(
                ticket_id=t_id,
                title=item.get("title", ""),
                category=item.get("category", "Other"),
                urgency=item.get("urgency", "low"),
                affected_users=item.get("affected_users", 1),
                assigned_to=item.get("assigned_to", "")
            )
            ticket["status"] = item.get("status", "open")
            
            # Restore notes if present
            raw_notes = item.get("notes", [])
            if not isinstance(raw_notes, list):
                raise ValueError(f"Ticket {t_id} notes field must be a list.")
            
            notes_list = []
            for n in raw_notes:
                if not isinstance(n, dict):
                    raise ValueError(f"Note in ticket {t_id} must be a dictionary.")
                n_id = n.get("note_id")
                author = n.get("author", "").strip()
                message = n.get("message", "").strip()
                if not n_id or not author or not message:
                    raise ValueError(f"Note in ticket {t_id} missing required fields (note_id, author, message).")
                notes_list.append({
                    "note_id": n_id,
                    "author": author,
                    "message": message
                })
            ticket["notes"] = notes_list
            validated_tickets.append(ticket)
        except Exception as e:
            raise ValueError(f"Validation failed for ticket '{t_id}': {e}")

    return validated_tickets

def get_next_ticket_id(tickets: list) -> str:
    """Determine the next sequential ticket ID (e.g., T001, T002...)."""
    max_num = 0
    for t in tickets:
        t_id = t.get("id", "")
        if t_id.startswith("T") and t_id[1:].isdigit():
            num = int(t_id[1:])
            if num > max_num:
                max_num = num
    return f"T{max_num + 1:03d}"
