# Command Chat Assistant (Python)

A Python application that uses the official GitHub Copilot SDK to answer questions about admin commands documented in `commands.md`.

## Features

- 🤖 Interactive chat interface powered by GitHub Copilot
- 📚 Context-aware responses based on commands documentation
- 💬 Async/await pattern for efficient API calls
- 🎯 Provides command syntax, parameters, and examples
- ✨ Uses the official GitHub Copilot SDK for Python

## Prerequisites

- Python 3.10 or higher
- GitHub Copilot license (individual, business, or enterprise)
- GitHub authentication

## Setup

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the virtual environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
.\venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Authenticate with GitHub

The Copilot SDK uses GitHub authentication. Make sure you're authenticated:

```bash
# Install GitHub CLI if not already installed
winget install GitHub.cli

# Authenticate
gh auth login
```

Alternatively, you can set a GitHub token:
```bash
# Set GITHUB_TOKEN environment variable
export GITHUB_TOKEN=your_github_token_here  # Linux/macOS
$env:GITHUB_TOKEN="your_github_token_here"  # PowerShell
```

## Usage

### Run the application

```bash
python command_chat_app.py
```

### Example Session

```
Loading commands from: commands.md
✓ RAG enabled: 8 chunks indexed, showing top 3 per query

✓ Copilot service initialized successfully

==================================================
  Command Chat Assistant - Powered by Copilot
==================================================
Ask me anything about the available commands!
Type 'exit' or 'quit' to end the session.

You: hwo to view sessions?
To view all active sessions, use the following command:

/session list

This command does not require any parameters. It will display a list of all currently active sessions, including their session IDs, users, and start times.

**Example Usage:**
```
/session list
```

**Example Response:**
```
Active Sessions:
1. Session ID: 12345, User: admin, Started: 2024-06-01 10:00 AM
2. Session ID: 67890, User: user1, Started: 2024-06-01 11:30 AM
```

Let me know if you need help with session termination or other session management commands!

You: show exchange info for NSE
To show information for the NSE (National Stock Exchange), use the following command:

/show exchange NSE

This will display details about the NSE, such as its location, timezone, and trading hours.

**Example Usage:**
```
/show exchange NSE
```

Let me know if you need information about a specific symbol or market as well!

You: show exchange info for TSE
To view information about the TSE (Tokyo Stock Exchange), use the following command:

/show exchange TSE

This will display details such as the exchange name, location, timezone, and trading hours.

**Example Usage:**
```
/show exchange TSE
```

Let me know if you need information about another exchange or a specific symbol!

You: how to terminate a session
To terminate a specific session, use the following command:

/session terminate <session_id>

Replace <session_id> with the actual ID of the session you want to terminate.

**Example Usage:**
```
/session terminate 12345
```

This will terminate the session with ID 12345.

If you want to terminate all active sessions, use:
/session terminate all

Let me know if you need help finding the session ID or have any other questions!

You: exit

Goodbye! Thanks for using Command Chat Assistant!
```

## Project Structure

```
copilot_sdk_command_chat_app/
├── command_chat_app.py          # Main application
├── commands.md                  # Commands documentation
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── venv/                        # Virtual environment (created after setup)
```

## How It Works

1. **CommandChatApp**: Main application class that:
   - Loads the commands.md file
   - Initializes the GitHub Copilot SDK Agent
   - Creates a session with commands context as system instructions
   - Provides an interactive console interface
   - Manages the async chat loop

2. **Agent**: GitHub Copilot SDK agent:
   - Connects to GitHub Copilot services
   - Uses GPT-4 model for responses
   - Maintains conversation context
   - Handles event-based messaging

3. **Context Injection**: The entire commands.md content is provided as system instructions when creating the agent, enabling accurate responses about documented commands.

## Troubleshooting

### Authentication Issues

If you see authentication errors:
```bash
# Check if you're authenticated
gh auth status

# Re-authenticate if needed
gh auth login
```

### Import Errors

If you get import errors with `copilot_sdk`:
```bash
# Make sure you're in the virtual environment
# Then reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Python Version

Make sure you're using Python 3.10 or higher:
```bash
python --version
```

## Configuration

### Change the Model

Edit `command_chat_app.py` and modify the model in the AgentConfig:
```python
config = AgentConfig(
    name="command-assistant",
    description="An assistant that helps with admin commands",
    instructions=system_message,
    model="gpt-4o"  # Change to "claude-sonnet-4.5", "o3-mini", etc.
)
```

### Use a Different Documentation File

Pass a different file path when creating the CommandChatApp:
```python
app = CommandChatApp("path/to/your/docs.md")
```

## Comparison with Java Version

✅ **Advantages over the Java implementation:**
- Uses the official GitHub Copilot SDK (actively maintained)
- Simpler async/await pattern
- No deprecated CLI dependencies
- Direct API access
- Better error handling
- Easier to set up and run

## License

This is a sample project for demonstration purposes.

## Resources

- [GitHub Copilot SDK Documentation](https://github.com/github/copilot-sdk)
- [GitHub Copilot API Documentation](https://docs.github.com/en/copilot)
- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
