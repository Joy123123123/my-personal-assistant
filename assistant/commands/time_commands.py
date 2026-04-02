from datetime import datetime


def handle_time(query: str) -> str:
    """Return the current time or date based on the query."""
    query_lower = query.lower()
    now = datetime.now()

    if "date" in query_lower:
        return f"Today's date is {now.strftime('%A, %B %d, %Y')}."
    if "time" in query_lower:
        return f"The current time is {now.strftime('%I:%M %p')}."
    if "day" in query_lower:
        return f"Today is {now.strftime('%A')}."
    if "year" in query_lower:
        return f"The current year is {now.strftime('%Y')}."
    if "month" in query_lower:
        return f"The current month is {now.strftime('%B')}."

    return (
        f"Right now it is {now.strftime('%I:%M %p')} on "
        f"{now.strftime('%A, %B %d, %Y')}."
    )
