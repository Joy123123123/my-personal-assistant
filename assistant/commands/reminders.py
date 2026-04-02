import json
import os
import re
from datetime import datetime
from typing import Optional

_DEFAULT_STORE = os.path.join(
    os.path.expanduser("~"), ".personal_assistant", "reminders.json"
)


def _load_reminders(store_path: str) -> list:
    if not os.path.exists(store_path):
        return []
    with open(store_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_reminders(reminders: list, store_path: str) -> None:
    os.makedirs(os.path.dirname(store_path), exist_ok=True)
    with open(store_path, "w", encoding="utf-8") as fh:
        json.dump(reminders, fh, indent=2)


def add_reminder(content: str, store_path: str = _DEFAULT_STORE) -> str:
    """Add a new reminder and return a confirmation message."""
    reminders = _load_reminders(store_path)
    reminder = {
        "id": len(reminders) + 1,
        "content": content.strip(),
        "created_at": datetime.now().isoformat(),
        "done": False,
    }
    reminders.append(reminder)
    _save_reminders(reminders, store_path)
    return f"Reminder #{reminder['id']} set: \"{reminder['content']}\""


def list_reminders(store_path: str = _DEFAULT_STORE) -> str:
    """Return a formatted list of all pending reminders."""
    reminders = _load_reminders(store_path)
    pending = [r for r in reminders if not r.get("done", False)]
    if not pending:
        return "You have no pending reminders."
    lines = ["Here are your reminders:"]
    for r in pending:
        lines.append(f"  #{r['id']}: {r['content']}")
    return "\n".join(lines)


def complete_reminder(reminder_id: int, store_path: str = _DEFAULT_STORE) -> str:
    """Mark a reminder as done and return a confirmation message."""
    reminders = _load_reminders(store_path)
    for r in reminders:
        if r["id"] == reminder_id:
            r["done"] = True
            _save_reminders(reminders, store_path)
            return f"Reminder #{reminder_id} marked as done."
    return f"Reminder #{reminder_id} not found."


def delete_reminder(reminder_id: int, store_path: str = _DEFAULT_STORE) -> str:
    """Delete a reminder by its ID and return a confirmation message."""
    reminders = _load_reminders(store_path)
    original_count = len(reminders)
    reminders = [r for r in reminders if r["id"] != reminder_id]
    if len(reminders) == original_count:
        return f"Reminder #{reminder_id} not found."
    _save_reminders(reminders, store_path)
    return f"Reminder #{reminder_id} deleted."


def handle_reminders(query: str, store_path: str = _DEFAULT_STORE) -> str:
    """Route a reminders-related query to the appropriate action."""
    query_lower = query.lower()

    if re.search(r"\b(list|show|view|display|all|my)\b", query_lower):
        return list_reminders(store_path)

    done_match = re.search(r"\b(done|complete|finish)\b.*?#?(\d+)", query_lower)
    if done_match:
        return complete_reminder(int(done_match.group(2)), store_path)

    delete_match = re.search(r"\bdelete\b.*?#?(\d+)", query_lower)
    if delete_match:
        return delete_reminder(int(delete_match.group(1)), store_path)

    add_match = re.search(
        r"(?:add|set|create|remind(?:\s+me)?)[:\s]+(?:to\s+)?(.+)",
        query,
        flags=re.IGNORECASE,
    )
    if add_match:
        return add_reminder(add_match.group(1).strip(), store_path)

    return (
        "I can help you with reminders! Try:\n"
        '  - "remind me to <task>"\n'
        '  - "list reminders"\n'
        '  - "done #<id>"\n'
        '  - "delete reminder #<id>"'
    )
