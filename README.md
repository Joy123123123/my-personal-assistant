# my-personal-assistant

A simple, extensible command-line personal assistant written in Python.

## Features

| Category | Commands |
|---|---|
| **Time & Date** | Ask the current time, date, day, month, or year |
| **Calculator** | Evaluate arithmetic expressions (+, -, *, /, %, ^) |
| **Notes** | Add, list, and delete personal notes |
| **Reminders** | Add, list, complete, and delete reminders |

## Requirements

- Python 3.8+

## Installation

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

Start the interactive CLI:

```bash
python main.py
```

### Example session

```
Hello! I'm Assistant, your personal assistant. Type 'help' to see what I can do.

You: What time is it?
Assistant: The current time is 02:30 PM.

You: calculate 2 ^ 10
Assistant: The result of 2**10 is 1024.

You: add note: Buy groceries
Assistant: Note #1 saved: "Buy groceries"

You: list notes
Assistant: Here are your notes:
  #1: Buy groceries

You: remind me to call mom
Assistant: Reminder #1 set: "call mom"

You: list reminders
Assistant: Here are your reminders:
  #1: call mom

You: done #1
Assistant: Reminder #1 marked as done.

You: bye
Assistant: Goodbye! Have a great day!
```

## Running Tests

```bash
python -m pytest tests/ -v
```

## Project Structure

```
my-personal-assistant/
├── assistant/
│   ├── __init__.py
│   ├── assistant.py          # Core Assistant class and query classifier
│   └── commands/
│       ├── __init__.py
│       ├── calculator.py     # Safe arithmetic expression evaluator
│       ├── notes.py          # Notes CRUD (stored in ~/.personal_assistant/)
│       ├── reminders.py      # Reminders CRUD (stored in ~/.personal_assistant/)
│       └── time_commands.py  # Time and date responses
├── tests/
│   ├── test_assistant.py
│   ├── test_calculator.py
│   ├── test_notes.py
│   ├── test_reminders.py
│   └── test_time_commands.py
├── main.py                   # CLI entry point
├── requirements.txt
└── setup.py
```
