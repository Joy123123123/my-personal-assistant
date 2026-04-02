#!/usr/bin/env python3
"""Entry point for the personal assistant CLI."""

import sys
from assistant import Assistant


def main() -> None:
    assistant = Assistant()
    print(assistant.greet())
    print()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n{assistant.name}: Goodbye!")
            sys.exit(0)

        if not user_input:
            continue

        response = assistant.respond(user_input)
        print(f"{assistant.name}: {response}")
        print()

        if user_input.lower() in {"bye", "goodbye", "exit", "quit", "farewell"}:
            sys.exit(0)


if __name__ == "__main__":
    main()
