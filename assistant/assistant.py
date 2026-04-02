import re
from .commands import handle_time, handle_calculator, handle_notes, handle_reminders

_GREETINGS = {"hi", "hello", "hey", "howdy", "greetings", "what's up", "sup"}

_FAREWELLS = {"bye", "goodbye", "exit", "quit", "see you", "later", "farewell"}

_HELP_TEXT = """\
I'm your personal assistant. Here's what I can do:

  Time & Date
    - "What time is it?"
    - "What's today's date?"
    - "What day is it?"

  Calculator
    - "Calculate 42 * 7"
    - "What is 100 / 4?"
    - "2 ^ 10"

  Notes
    - "Add note: Buy groceries"
    - "List notes"
    - "Delete note #2"

  Reminders
    - "Remind me to call mom"
    - "List reminders"
    - "Done #1"
    - "Delete reminder #3"

  General
    - "Help" — show this message
    - "Bye" — exit the assistant
"""


def _classify(query: str) -> str:
    """Return a category label for the given user query."""
    q = query.lower().strip().rstrip("!?.,")

    if q in _GREETINGS or any(q.startswith(g + " ") for g in _GREETINGS):
        return "greeting"
    if q in _FAREWELLS or any(q.startswith(f + " ") for f in _FAREWELLS):
        return "farewell"
    if re.search(r"\bhelp\b", q):
        return "help"

    time_keywords = r"\b(time|date|day|today|year|month|clock|when)\b"
    if re.search(time_keywords, q):
        return "time"

    calc_keywords = (
        r"\b(calculat|comput|eval|math|plus|minus|times|divided?|"
        r"percent|square|sqrt|pow|result)\b"
        r"|[\d]+\s*[\+\-\*/\^%]\s*[\d]+"
    )
    if re.search(calc_keywords, q):
        return "calculator"

    note_keywords = r"\bnote[s]?\b"
    if re.search(note_keywords, q):
        return "notes"

    reminder_keywords = r"\bremind(er[s]?|ing)?\b"
    if re.search(reminder_keywords, q):
        return "reminders"

    return "unknown"


class Assistant:
    """A simple rule-based personal assistant."""

    def __init__(self, name: str = "Assistant") -> None:
        self.name = name

    def greet(self) -> str:
        return f"Hello! I'm {self.name}, your personal assistant. Type 'help' to see what I can do."

    def respond(self, query: str) -> str:
        """Process a query string and return a response."""
        query = query.strip()
        if not query:
            return "Please say something!"

        category = _classify(query)

        if category == "greeting":
            return f"Hello! How can I help you today?"
        if category == "farewell":
            return "Goodbye! Have a great day!"
        if category == "help":
            return _HELP_TEXT
        if category == "time":
            return handle_time(query)
        if category == "calculator":
            return handle_calculator(query)
        if category == "notes":
            return handle_notes(query)
        if category == "reminders":
            return handle_reminders(query)

        return (
            "I'm not sure I understand. Type 'help' to see what I can do, "
            "or try rephrasing your request."
        )
