"""Core ticket rules. No input() or print() here, so it is easy to test."""

from campusflow.validation import (
    validate_title,
    validate_category,
    validate_urgency,
    validate_affected_users,
    validate_staff,
)

ALLOWED_TRANSITIONS = {
    "open": {"in_progress"},
    "in_progress": {"resolved"},
    "resolved": {"open"},  # reopen
}

PRIORITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"
    if urgency == "high" or affected_users >= 10:
        return "high"
    if urgency == "medium" or affected_users >= 3:
        return "medium"
    return "low"


def next_ticket_id(tickets):
    # Compare the NUMBER, not the text, so T10 comes after T2.
    numbers = [int(t["id"][1:]) for t in tickets]
    return f"T{max(numbers, default=0) + 1:03d}"


def create_ticket(tickets, title, category, urgency, affected_users):
    """Validate everything FIRST, then add the ticket. Raises ValueError if invalid."""
    title = validate_title(title)
    category = validate_category(category)
    urgency = validate_urgency(urgency)
    affected_users = validate_affected_users(affected_users)

    ticket = {
        "id": next_ticket_id(tickets),
        "title": title,
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
        "priority": calculate_priority(urgency, affected_users),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }
    tickets.append(ticket)  # the only mutation, after all checks pass
    return ticket


def find_ticket(tickets, ticket_id):
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket
    raise ValueError(f"Ticket {ticket_id} not found.")


def assign_ticket(tickets, ticket_id, staff):
    """Validate first, mutate last. Raises ValueError and changes nothing if invalid."""
    ticket = find_ticket(tickets, ticket_id)
    staff = validate_staff(staff)
    if ticket["status"] == "resolved":
        raise ValueError("Resolved tickets cannot be reassigned. Reopen it first.")
    ticket["assigned_to"] = staff
    return ticket


def change_status(tickets, ticket_id, new_status):
    ticket = find_ticket(tickets, ticket_id)
    if new_status not in ALLOWED_TRANSITIONS.get(ticket["status"], set()):
        raise ValueError(f"Cannot move from {ticket['status']} to {new_status}.")
    if new_status == "in_progress" and not ticket["assigned_to"]:
        raise ValueError("Assign the ticket before moving it to in_progress.")
    ticket["status"] = new_status
    return ticket


def open_work_queue(tickets):
    """Only OPEN tickets, by priority (critical first), then by NUMERIC id.
    Returns a new list; does not modify `tickets`."""
    open_tickets = [t for t in tickets if t["status"] == "open"]
    return sorted(
        open_tickets,
        key=lambda t: (PRIORITY_RANK[t["priority"]], int(t["id"][1:])),
    )
