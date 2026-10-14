# campusflow/notes.py

def validate_note_message(message: str) -> str:
    """Validate message length must be 5-300 characters after trimming."""
    if not isinstance(message, str):
        raise TypeError("Note message must be a string.")
    cleaned = message.strip()
    if len(cleaned) < 5 or len(cleaned) > 300:
        raise ValueError("Note message must be between 5 and 300 characters.")
    return cleaned

def validate_note_author(author: str) -> str:
    """Validate author label cannot be blank."""
    if not isinstance(author, str):
        raise TypeError("Author must be a string.")
    cleaned = author.strip()
    if not cleaned:
        raise ValueError("Author label cannot be blank.")
    return cleaned

def add_note_to_ticket(ticket: dict, author: str, message: str) -> dict:
    """
    Add a follow-up note to a ticket.
    Requirements:
    - Ticket status must be 'open' or 'in_progress'. Resolved tickets reject notes.
    - Author must not be blank.
    - Message must be 5-300 characters.
    - Note IDs generated sequentially as N001, N002, etc. per ticket.
    - Failed validation must not consume a note ID or mutate the ticket.
    """
    if ticket.get("status") not in {"open", "in_progress"}:
        raise ValueError("Cannot add notes to a resolved ticket unless it is reopened.")
    
    clean_author = validate_note_author(author)
    clean_msg = validate_note_message(message)
    
    notes = ticket.setdefault("notes", [])
    next_num = len(notes) + 1
    note_id = f"N{next_num:03d}"
    
    new_note = {
        "note_id": note_id,
        "author": clean_author,
        "message": clean_msg
    }
    
    notes.append(new_note)
    return new_note
