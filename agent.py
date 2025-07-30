from __future__ import annotations
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    RunContext,
    WorkerOptions,
    cli,
    function_tool
)
from livekit.plugins import openai, silero
from assistant_functions import AssistantFnc
from prompts import WELCOME_MESSAGE, INSTRUCTIONS
import os
import asyncio
from livekit import api

# LiveKit configuration - use environment variables or fallback to defaults
LIVEKIT_URL = os.environ.get("LIVEKIT_URL", "wss://launch-65q9o9la.livekit.cloud")
LIVEKIT_API_KEY = os.environ.get("LIVEKIT_API_KEY", "APIBAfXa36Hgo2j")
LIVEKIT_API_SECRET = os.environ.get("LIVEKIT_API_SECRET", "hLSaGpDgyKProcV263Ddvl3ceWemIXa0qKI91sAiAgL")

# OpenAI configuration
if "OPENAI_API_KEY" not in os.environ:
    raise ValueError("Please set the OPENAI_API_KEY environment variable")

class SocialWorkerAssistant(Agent):
    def __init__(self, assistant_fnc: AssistantFnc) -> None:
        super().__init__(
            instructions=INSTRUCTIONS
        )
        self.assistant_fnc = assistant_fnc
        
    @function_tool()
    async def lookup_client(self, context: RunContext, client_id: str) -> dict:
        """Look up a client by their ID number.
        
        Args:
            client_id: The client ID to look up
        """
        return await self.assistant_fnc.lookup_client(client_id)
        
    @function_tool()
    async def get_case_history(self, context: RunContext) -> dict:
        """Get the case history for the current client."""
        return await self.assistant_fnc.get_case_history()
        
    @function_tool()
    async def get_available_resources(self, context: RunContext) -> dict:
        """Get information about available resources and programs in Houston."""
        return await self.assistant_fnc.get_available_resources()
    
    @function_tool()
    async def translate_text(self, context: RunContext, text: str, target_language: str) -> dict:
        """Translate text to the specified language.
        
        Args:
            text: The text to translate
            target_language: Target language (e.g., 'Spanish', 'French', 'Vietnamese', etc.)
        """
        return await self.assistant_fnc.translate_text(text, target_language)
    
    @function_tool()
    async def get_platform_features(self, context: RunContext) -> dict:
        """Get comprehensive information about NextStep platform features and capabilities."""
        return await self.assistant_fnc.get_platform_features()
    
    @function_tool()
    async def search_resources_by_category(self, context: RunContext, category: str) -> dict:
        """Search for resources by specific category.
        
        Args:
            category: Resource category ('housing', 'food', 'transportation')
        """
        return await self.assistant_fnc.search_resources_by_category(category)
    
    @function_tool()
    async def get_client_statistics(self, context: RunContext) -> dict:
        """Get statistics and analytics about clients in the system."""
        return await self.assistant_fnc.get_client_statistics()

async def entrypoint(ctx: JobContext):
    try:
        print("Connecting to room...")
        await ctx.connect()
        print("Connected to room successfully")
        
        assistant_fnc = AssistantFnc()
        agent = SocialWorkerAssistant(assistant_fnc)
        print("Created agent instance")
        
        # Initialize the session with proper configuration
        session = AgentSession(
            vad=silero.VAD.load(),
            stt=openai.STT(model="whisper-1"),
            llm=openai.LLM(model="gpt-4o"),
            tts=openai.TTS(voice="shimmer", model="tts-1"),
        )
        print("Created agent session")

        print("Starting session...")
        await session.start(
            agent=agent,
            room=ctx.room
        )
        print("Session started successfully")
        
        # Wait a moment for the session to fully initialize
        await asyncio.sleep(1)
        
        print("Saying welcome message...")
        await session.say(WELCOME_MESSAGE, allow_interruptions=True)
        print("Welcome message sent")
        
    except Exception as e:
        print(f"Error in entrypoint: {e}")
        raise

if __name__ == "__main__":
    # Set up the worker options with the correct URL format
    api_url = LIVEKIT_URL.replace("wss://", "https://")
    ws_url = LIVEKIT_URL  # Don't append any path, use the base URL
    
    options = WorkerOptions(
        entrypoint_fnc=entrypoint,
        ws_url=ws_url,
        api_key=LIVEKIT_API_KEY,
        api_secret=LIVEKIT_API_SECRET,
        port=8083  # Use a different port
    )
    print(f"Starting agent with WebSocket URL: {ws_url}")
    print(f"API URL: {api_url}")
    cli.run_app(options)