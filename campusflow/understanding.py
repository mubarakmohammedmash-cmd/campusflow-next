# campusflow/understanding.py

QUESTIONS = [
    {
        "id": "Q1",
        "question": "Ticket T001 is open and unassigned. A user tries to move it to in_progress. What should happen?",
        "options": {
            "A": "Accept",
            "B": "Reject and preserve all data",
            "C": "Resolve it automatically",
            "D": "Remove ticket"
        },
        "answer": "B"
    },
    {
        "id": "Q2",
        "question": "The app has zero tickets. What should resolution percentage display?",
        "options": {
            "A": "Crash",
            "B": "100%",
            "C": "0%",
            "D": "Divide by one without explanation"
        },
        "answer": "C"
    },
    {
        "id": "Q3",
        "question": "Filter title='wifi', category='Network', status='open'. Which records should match?",
        "options": {
            "A": "Any record matching one filter",
            "B": "Only records matching all supplied filters",
            "C": "All network records",
            "D": "All open records"
        },
        "answer": "B"
    },
    {
        "id": "Q4",
        "question": "A resolved ticket receives 'Add note'. What should happen?",
        "options": {
            "A": "Append anyway",
            "B": "Delete old notes",
            "C": "Reject until reopened",
            "D": "Change status silently"
        },
        "answer": "C"
    },
    {
        "id": "Q5",
        "question": "The JSON file includes two tickets with the same ID. What should load do?",
        "options": {
            "A": "Keep both",
            "B": "Replace memory with duplicates",
            "C": "Reject the load without changing current memory",
            "D": "Rename IDs silently"
        },
        "answer": "C"
    },
    {
        "id": "Q6",
        "question": "A PR changes validation but has no negative-case tests. Best review action?",
        "options": {
            "A": "Approve because it runs",
            "B": "Request focused tests and reasoning",
            "C": "Merge immediately",
            "D": "Ask AI to approve it"
        },
        "answer": "B"
    }
]

def run_understanding_check(input_func=input, print_func=print) -> int:
    """Interactive menu containing 6 multiple-choice scenario questions. Returns score (0-6)."""
    score = 0
    print_func("\n=== ENGINEERING UNDERSTANDING CHECK ===")
    
    for q in QUESTIONS:
        print_func(f"\n{q['id']}: {q['question']}")
        for opt, text in q["options"].items():
            print_func(f"  {opt}. {text}")
        
        while True:
            choice = input_func("Your choice (A/B/C/D): ").strip().upper()
            if choice in {"A", "B", "C", "D"}:
                break
            print_func("Invalid choice. Please enter A, B, C, or D.")
        
        if choice == q["answer"]:
            print_func("✓ Correct!")
            score += 1
        else:
            print_func(f"✗ Incorrect. The correct answer was {q['answer']}.")
    
    print_func(f"\nFinal Score: {score}/6")
    return score
