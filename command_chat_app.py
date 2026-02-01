"""
Command Chat Assistant - Powered by GitHub Copilot SDK

A chat application that uses GitHub Copilot SDK to answer questions
about commands documented in commands.md file.
"""

import asyncio
from pathlib import Path
import sys
from utils.property_loader import PropertyLoader
from rag_engine import RAGEngine
from copilot_service import CopilotService


class CommandChatApp:
    def __init__(self, commands: str, properties: PropertyLoader, 
                 copilot_service: CopilotService, rag_engine: RAGEngine | None = None):
        """Initialize the Command Chat Assistant."""
        self.commands_context = commands
        self.properties = properties
        self.copilot_service = copilot_service
        self.rag_engine = rag_engine
        self.loading = False
           
    async def initialize(self):
        """Initialize the Copilot service with appropriate context."""
        system_prompt = self.properties.get_property("messages", "system.prompt")
        
        # Use full context if RAG is disabled
        if self.rag_engine is None:
            system_message = f"{system_prompt}\n\nCommands Documentation:\n{self.commands_context}"
        else:
            # With RAG, context is injected per query
            system_message = system_prompt
        
        await self.copilot_service.initialize(system_message)
        print("✓ Copilot service initialized successfully\n")
    
    async def show_loading_spinner(self):
        """Display a loading spinner while waiting for response."""
        spinner_str = self.properties.get_property("app", "spinner.chars")
        spinner_chars = spinner_str.split(",")
        idx = 0
        while self.loading:
            sys.stdout.write(f"\r{spinner_chars[idx % len(spinner_chars)]} ") # type: ignore
            sys.stdout.flush() # type: ignore
            idx += 1
            await asyncio.sleep(0.1)
    
    async def get_command_answer(self, query: str) -> None:
        """Get an answer from Copilot based on the user query."""
        try:
            self.loading = True
            first_token = True
            
            # Start spinner task
            spinner_task = asyncio.create_task(self.show_loading_spinner())
            
            # Build the prompt with RAG context if enabled
            if self.rag_engine:
                relevant_context = self.rag_engine.get_context_for_query(query)
                full_prompt = f"{query}\n\nRelevant Documentation:\n{relevant_context}"
            else:
                full_prompt = query
            
            # Callback to display tokens as they arrive
            def on_token(token: str):
                nonlocal first_token
                if first_token:
                    # Stop spinner on first token
                    self.loading = False
                    first_token = False
                    sys.stdout.write("\r" + " " * 20 + "\r")  # type: ignore
                sys.stdout.write(token)  # type: ignore
                sys.stdout.flush()  # type: ignore
            
            # Send query with streaming callback
            _ = await self.copilot_service.send_query(full_prompt, on_token=on_token)
            
            # Ensure spinner is stopped
            self.loading = False
            await spinner_task
            
            print()  # New line after response
            
        except Exception as e:
            self.loading = False
            print(f"Error getting response: {str(e)}")
    
    async def start_chat(self):
        """Start the interactive chat session."""
        print("=" * 50)
        print("  Command Chat Assistant - Powered by Copilot")
        print("=" * 50)
        print("Ask me anything about the available commands!")
        print("Type 'exit' or 'quit' to end the session.\n")
        
        while True:
            try:
                user_query = await asyncio.to_thread(input, "You: ")
                user_query = user_query.strip()
                if not user_query:
                    continue
                
                # Check for exit commands
                if user_query.lower() in ['exit', 'quit']:
                    goodbye_msg = self.properties.get_property("messages", "goodbye")
                    print(f"\n{goodbye_msg}")
                    break
                
                # Get response from Copilot
                await self.get_command_answer(user_query)
                print()  # Extra line for spacing
                
            except KeyboardInterrupt | EOFError:
                goodbye_msg = self.properties.get_property("messages", "goodbye")
                print(f"\n\n{goodbye_msg}")
                break
            except Exception as e:
                print(f"\nError: {e}\n")
        
        # Clean up
        await self.copilot_service.close()


def load_commands_file(commands_file) -> str:
    """Load the commands.md file content."""
    try:
        commands_path = Path(commands_file)
        if not commands_path.exists():
            raise FileNotFoundError(f"Commands file not found: {commands_file}")
        return commands_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error loading commands file: {e}")
        sys.exit(1)


async def main():
    """Main entry point for the application."""
    try:
        properties = PropertyLoader("config/app.properties")
        
        loading_msg = properties.get_property("app", "loading.message")
        print(loading_msg)
        
        # Load commands file
        commands = load_commands_file(properties.get_property("app", "commands.file"))
        
        # Initialize RAG engine if enabled
        rag_enabled = properties.get_property("rag", "enabled").lower() == "true"
        rag_engine = None
        
        if rag_enabled:
            max_chunks = int(properties.get_property("rag", "max.chunks"))
            rag_engine = RAGEngine(commands, max_chunks=max_chunks)
            stats = rag_engine.get_stats()
            print(f"✓ RAG enabled: {stats['total_chunks']} chunks indexed, showing top {max_chunks} per query\n")
        else:
            print("✓ RAG disabled: Using full document context\n")
        
        # Create Copilot service
        model = properties.get_property("app", "model")
        copilot_service = CopilotService(model=model)

        # Create and initialize the chat application
        app = CommandChatApp(commands, properties, copilot_service, rag_engine)
        await app.initialize()
        
        # Start the interactive chat
        await app.start_chat()
        
    except Exception as e:
        print(f"Error initializing application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
