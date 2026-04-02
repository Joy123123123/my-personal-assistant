# Personal Terminal Assistant

A minimal, safe terminal assistant for Codespaces that understands English and Bangla commands.

## Features

- ✅ **Safe Command Whitelist**: Only allows `ls`, `pwd`, `cat`, `echo`, `python`, `pip`, `mkdir`, `touch`, `cp`, `mv`, `grep`
- 🚫 **Dangerous Command Blocking**: Blocks `rm -rf`, `shutdown`, `reboot`, `dd`, `mkfs`, fork bombs, etc.
- 🧠 **Memory**: Keeps conversation history in `memory.json`
- 🌍 **Bilingual**: Accepts instructions in English and Bangla

## Requirements

- Python 3
- Linux terminal (Codespaces)

## Setup and Run

### 1. Make the script executable (optional):
```bash
chmod +x agent.py
```

### 2. Run the assistant:
```bash
python3 agent.py
```

Or directly:
```bash
./agent.py
```

## Usage Examples

### English Commands:
```
You: list files
You: show current directory
You: ls -la
You: pwd
You: echo Hello World
```

### Bangla Commands:
```
You: ফাইল দেখাও
You: কোথায় আছি
You: ls
```

### Direct Commands:
```
You: ls -la
You: cat memory.json
You: mkdir test
You: touch newfile.txt
```

### Exit:
```
You: exit
You: quit
You: bye
```

## Security

The assistant will **block** dangerous commands such as:
- `rm -rf /`
- `shutdown`
- `reboot`
- `dd if=/dev/zero of=/dev/sda`
- `mkfs`
- Fork bombs: `:(){ :|:& };:`

Only whitelisted commands are allowed to execute.

## Memory

All interactions are saved in `memory.json` with:
- Timestamp
- User input
- Executed command
- Output (truncated to 500 chars)
- Status (success/failed/blocked)

The last 100 conversations are kept in memory.

## Files

- `agent.py` - Main assistant script
- `memory.json` - Conversation history storage
- `README.md` - This file
