import json
import os
import re
from datetime import datetime
from typing import Optional

_DEFAULT_STORE = os.path.join(
    os.path.expanduser("~"), ".personal_assistant", "notes.json"
)


def _load_notes(store_path: str) -> list:
    if not os.path.exists(store_path):
        return []
    with open(store_path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _save_notes(notes: list, store_path: str) -> None:
    os.makedirs(os.path.dirname(store_path), exist_ok=True)
    with open(store_path, "w", encoding="utf-8") as fh:
        json.dump(notes, fh, indent=2)


def add_note(content: str, store_path: str = _DEFAULT_STORE) -> str:
    """Add a new note and return a confirmation message."""
    notes = _load_notes(store_path)
    note = {
        "id": len(notes) + 1,
        "content": content.strip(),
        "created_at": datetime.now().isoformat(),
    }
    notes.append(note)
    _save_notes(notes, store_path)
    return f"Note #{note['id']} saved: \"{note['content']}\""


def list_notes(store_path: str = _DEFAULT_STORE) -> str:
    """Return a formatted list of all notes."""
    notes = _load_notes(store_path)
    if not notes:
        return "You have no notes yet."
    lines = ["Here are your notes:"]
    for n in notes:
        lines.append(f"  #{n['id']}: {n['content']}")
    return "\n".join(lines)


def delete_note(note_id: int, store_path: str = _DEFAULT_STORE) -> str:
    """Delete a note by its ID and return a confirmation message."""
    notes = _load_notes(store_path)
    original_count = len(notes)
    notes = [n for n in notes if n["id"] != note_id]
    if len(notes) == original_count:
        return f"Note #{note_id} not found."
    _save_notes(notes, store_path)
    return f"Note #{note_id} deleted."


def handle_notes(query: str, store_path: str = _DEFAULT_STORE) -> str:
    """Route a notes-related query to the appropriate action."""
    query_lower = query.lower()

    if re.search(r"\b(list|show|view|display|all|my)\b", query_lower):
        return list_notes(store_path)

    delete_match = re.search(r"\bdelete\b.*?#?(\d+)", query_lower)
    if delete_match:
        return delete_note(int(delete_match.group(1)), store_path)

    add_match = re.search(
        r"(?:add|save|create|take|write|make)\s+(?:a\s+)?note[:\s]+(.+)",
        query,
        flags=re.IGNORECASE,
    )
    if add_match:
        return add_note(add_match.group(1).strip(), store_path)

    quoted_match = re.search(r'"(.+?)"|\'(.+?)\'', query)
    if quoted_match:
        content = quoted_match.group(1) or quoted_match.group(2)
        return add_note(content, store_path)

    return (
        "I can help you with notes! Try:\n"
        '  - "add note: <your note>"\n'
        '  - "list notes"\n'
        '  - "delete note #<id>"'
    )
