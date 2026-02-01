"""
Copilot Service - Handles all GitHub Copilot SDK interactions

This service manages the Copilot client lifecycle and message sending,
completely separated from UI concerns.
"""

import asyncio
from collections.abc import Callable
from copilot import CopilotClient
from copilot.generated.session_events import SessionEventType


class CopilotService:
    """Service class for managing Copilot SDK interactions."""
    
    def __init__(self, model: str = "gpt-4.1"):
        """
        Initialize the Copilot service.
        
        Args:
            model: The model to use for responses
        """
        self.model = model
        self.client: CopilotClient | None = None
        self.session = None
        self._response_buffer: list[str] = []
        self._is_streaming = False
    
    async def initialize(self, system_message: str) -> None:
        """
        Initialize the Copilot client and create a session.
        
        Args:
            system_message: The system prompt/context for the session
        """
        self.client = CopilotClient()
        await self.client.start()
        
        self.session = await self.client.create_session({
            "model": self.model,
            "streaming": True,
            "system_message": {"mode": "replace", "content": system_message}
        })  # type: ignore
        
        # Register event handler
        def handle_event(event):
            if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
                self._response_buffer.append(event.data.delta_content)
            if event.type == SessionEventType.SESSION_IDLE:
                self._is_streaming = False
        
        self.session.on(handle_event)  # type: ignore
    
    async def send_query(self, query: str, on_token: Callable[[str], None] | None = None) -> str:
        """
        Send a query to Copilot and get the response.
        
        Args:
            query: The user's question
            on_token: Optional callback for streaming tokens (called with each token)
            
        Returns:
            The complete response text
        """
        if not self.session:
            raise RuntimeError("Service not initialized. Call initialize() first.")
        
        # Clear previous response
        self._response_buffer.clear()
        self._is_streaming = True
        
        # If streaming callback provided, monitor buffer and call it
        async def stream_monitor():
            last_position = 0
            while self._is_streaming or last_position < len(self._response_buffer):
                if last_position < len(self._response_buffer):
                    # New tokens available
                    new_tokens = self._response_buffer[last_position:]
                    for token in new_tokens:
                        if on_token:
                            on_token(token)
                    last_position = len(self._response_buffer)
                await asyncio.sleep(0.01)  # Small delay to avoid busy waiting
        
        # Start streaming monitor if callback provided
        monitor_task = None
        if on_token:
            monitor_task = asyncio.create_task(stream_monitor())
        
        # Send query
        await self.session.send_and_wait({"prompt": query})  # type: ignore
        
        # Wait for streaming monitor to finish
        if monitor_task:
            await monitor_task
        
        # Return complete response
        return "".join(self._response_buffer)
    
    async def close(self) -> None:
        """Clean up and close the Copilot client."""
        if self.client:
            await self.client.stop()  # type: ignore
    
    def is_ready(self) -> bool:
        """Check if the service is initialized and ready."""
        return self.client is not None and self.session is not None
