#!/usr/bin/env python3
"""
Personal Terminal Assistant
A safe terminal assistant that accepts commands in English and Bangla.
"""

import json
import os
import subprocess
import sys
import re
from datetime import datetime

# Safe command whitelist
SAFE_COMMANDS = ['ls', 'pwd', 'cat', 'echo', 'python', 'pip', 'mkdir', 'touch', 'cp', 'mv', 'grep']

# Dangerous command patterns to block
DANGEROUS_PATTERNS = [
    r'\brm\s+-rf\b',
    r'\brm\s+-fr\b',
    r'\brm\s+.*-[rR].*f',
    r'\brm\s+.*-[fF].*r',
    r'\bshutdown\b',
    r'\breboot\b',
    r'\bdd\b',
    r'\bmkfs\b',
    r':\(\)\{.*:\|:.*\}',  # fork bomb pattern
    r'\bformat\b',
    r'\binit\s+0\b',
    r'\bkill\s+-9\s+-1\b',
]

MEMORY_FILE = 'memory.json'


class TerminalAssistant:
    def __init__(self):
        self.memory = self.load_memory()

    def load_memory(self):
        """Load conversation history from memory.json"""
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Could not load memory: {e}")
                return {"conversations": [], "last_updated": ""}
        return {"conversations": [], "last_updated": ""}

    def save_memory(self):
        """Save conversation history to memory.json"""
        self.memory["last_updated"] = datetime.now().isoformat()
        try:
            with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.memory, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️  Warning: Could not save memory: {e}")

    def add_to_memory(self, user_input, command, output, status):
        """Add interaction to memory"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "command": command,
            "output": output[:500] if output else "",  # Limit output size
            "status": status
        }
        self.memory["conversations"].append(entry)
        # Keep only last 100 entries
        if len(self.memory["conversations"]) > 100:
            self.memory["conversations"] = self.memory["conversations"][-100:]
        self.save_memory()

    def is_dangerous(self, command):
        """Check if command contains dangerous patterns"""
        for pattern in DANGEROUS_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return True
        return False

    def is_safe_command(self, command):
        """Check if command starts with a whitelisted command"""
        command_parts = command.strip().split()
        if not command_parts:
            return False

        base_command = command_parts[0]

        # Handle python3 as alias for python
        if base_command == 'python3':
            return True

        return base_command in SAFE_COMMANDS

    def parse_input(self, user_input):
        """Parse user input in English or Bangla and extract command"""
        # Common Bangla instruction patterns
        bangla_patterns = {
            r'দেখাও|দেখান|দেখা': 'ls',  # show
            r'কোথায়|কোন ডিরেক্টরি': 'pwd',  # where/which directory
            r'ফাইল পড়ো|পড়ুন|দেখাও': 'cat',  # read file
            r'বলো|বল|প্রিন্ট': 'echo',  # say/print
            r'তৈরি করো|বানাও': 'mkdir',  # create/make
        }

        # Check for direct commands
        if user_input.strip().startswith(tuple(SAFE_COMMANDS)) or user_input.strip().startswith('python3'):
            return user_input.strip()

        # Try to extract from natural language (both English and Bangla)
        lower_input = user_input.lower()

        # English patterns
        if 'list' in lower_input or 'show files' in lower_input:
            return 'ls -la' if 'all' in lower_input or 'hidden' in lower_input else 'ls'
        elif 'current directory' in lower_input or 'where am i' in lower_input:
            return 'pwd'
        elif 'show' in lower_input and 'file' in lower_input:
            # Try to extract filename
            words = user_input.split()
            for i, word in enumerate(words):
                if word.lower() in ['file', 'ফাইল'] and i + 1 < len(words):
                    return f'cat {words[i+1]}'
            return 'cat'

        # Bangla patterns
        for pattern, cmd in bangla_patterns.items():
            if re.search(pattern, user_input):
                if cmd == 'cat' and 'ফাইল' in user_input:
                    # Try to extract filename
                    words = user_input.split()
                    for i, word in enumerate(words):
                        if 'ফাইল' in word and i + 1 < len(words):
                            return f'cat {words[i+1]}'
                return cmd

        # If no pattern matched, return the input as-is (might be a direct command)
        return user_input.strip()

    def execute_command(self, command):
        """Execute a safe command"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            output = result.stdout + result.stderr
            return output.strip(), result.returncode == 0
        except subprocess.TimeoutExpired:
            return "⏱️  Command timed out (30s limit)", False
        except Exception as e:
            return f"❌ Error executing command: {str(e)}", False

    def process_request(self, user_input):
        """Process user request and execute command safely"""
        if not user_input.strip():
            return "Please enter a command or instruction.", False

        # Parse the input to extract command
        command = self.parse_input(user_input)

        # Check for dangerous patterns
        if self.is_dangerous(command):
            msg = "🚫 BLOCKED: Dangerous command detected! This command is not allowed."
            self.add_to_memory(user_input, command, msg, "blocked")
            return msg, False

        # Check if it's a whitelisted command
        if not self.is_safe_command(command):
            msg = f"🚫 BLOCKED: Command '{command.split()[0] if command.split() else command}' is not in the safe whitelist.\nAllowed commands: {', '.join(SAFE_COMMANDS)}"
            self.add_to_memory(user_input, command, msg, "blocked")
            return msg, False

        # Execute the command
        output, success = self.execute_command(command)
        status = "success" if success else "failed"

        self.add_to_memory(user_input, command, output, status)

        return output, success

    def run(self):
        """Main interactive loop"""
        print("🤖 Personal Terminal Assistant")
        print("=" * 50)
        print("I can help you with safe terminal commands.")
        print("Speak to me in English or Bangla!")
        print(f"✅ Safe commands: {', '.join(SAFE_COMMANDS)}")
        print("Type 'exit', 'quit', or 'bye' to exit.")
        print("=" * 50)
        print()

        while True:
            try:
                user_input = input("You: ").strip()

                # Check for exit commands
                if user_input.lower() in ['exit', 'quit', 'bye', 'বাই', 'বের হও']:
                    print("👋 Goodbye! আবার দেখা হবে!")
                    break

                if not user_input:
                    continue

                # Process the request
                output, success = self.process_request(user_input)

                # Display output
                if output:
                    print(f"\n🖥️  Output:\n{output}\n")
                else:
                    print("✓ Command executed (no output)\n")

            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except EOFError:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Unexpected error: {e}\n")


def main():
    assistant = TerminalAssistant()
    assistant.run()


if __name__ == "__main__":
    main()
