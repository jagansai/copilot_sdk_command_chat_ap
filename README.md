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

### Example Interactions

**Example 1: Ask about a specific command**
```
You: How do I list all active sessions?
Assistant: To list all active sessions, use the command `/session list`. 
This command doesn't require any parameters and will show you all active 
sessions with their Session ID, User, Start Time, and Status.

Example: `/session list`
```

**Example 2: Ask about parameters**
```
You: What parameters does the user create command need?
Assistant: The `/user create` command requires three parameters:
- username (String, Required): The desired username
- email (String, Required): User's email address
- role (String, Required): User role (admin, moderator, user)

Example usage: `/user create john.doe john.doe@example.com moderator`
```

**Example 3: General questions**
```
You: How can I backup the database?
Assistant: To backup the database, use the `/db backup` command.
You can optionally provide a custom name with the --name parameter.

Examples:
- `/db backup` (auto-generated timestamp name)
- `/db backup --name pre-migration-backup` (custom name)

The command will return the backup file location and size.
```

**Example 4: Exit the chat**
```
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
