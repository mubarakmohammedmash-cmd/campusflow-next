# campusflow/search.py

def search_tickets(tickets: list, query: str = "", category: str = "", status: str = "", priority: str = "", urgency: str = "") -> list:
    """
    Search and filter tickets using logical AND.
    Read-only: does not modify records.
    """
    results = []
    
    q_clean = query.strip().casefold()
    cat_clean = category.strip().capitalize() if category else ""
    stat_clean = status.strip().lower() if status else ""
    prio_clean = priority.strip().lower() if priority else ""
    urg_clean = urgency.strip().lower() if urgency else ""

    for ticket in tickets:
        if q_clean and q_clean not in ticket.get("title", "").casefold():
            continue
        if cat_clean and ticket.get("category") != cat_clean:
            continue
        if stat_clean and ticket.get("status") != stat_clean:
            continue
        if prio_clean and ticket.get("priority") != prio_clean:
            continue
        if urg_clean and ticket.get("urgency") != urg_clean:
            continue
        results.append(ticket)
        
    return results
