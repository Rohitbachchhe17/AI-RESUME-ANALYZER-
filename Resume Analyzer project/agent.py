import logging
import os
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.agents.voice import Agent, AgentSession
from livekit.plugins import openai, sarvam, elevenlabs

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

class VoiceAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            # Your agent's personality and instructions
            instructions="""
                You are a helpful voice assistant.
                Be friendly, concise, and conversational.
                Speak naturally as if you're having a real conversation.
            """,
            
            # Saaras v3 STT - Converts speech to text
            stt=sarvam.STT(
                language="unknown",  # Auto-detect language, or use "en-IN", "hi-IN", etc.
                model="saaras:v3",
                mode="transcribe",
                flush_signal=True  # Enables speech start/end events
            ),
            
            # OpenAI LLM - The "brain" that processes and generates responses
            # We configure base_url via OPENAI_BASE_URL env var to use OpenRouter
            llm=openai.LLM(
                model="openai/gpt-4o-mini" if "openrouter" in os.getenv("OPENAI_BASE_URL", "") else "gpt-4o-mini",
            ),
            
            # ElevenLabs TTS - Converts text to speech using the specified voice ID
            tts=elevenlabs.TTS(
                model="eleven_multilingual_v2",
                voice=elevenlabs.Voice(
                    id="JBFqnCBsd6RMkjVDRZzb",
                    name="Bostonian",
                    category="premade",
                )
            ),
        )
    
    async def on_enter(self):
        """Called when user joins - agent starts the conversation"""
        self.session.generate_reply()

async def entrypoint(ctx: JobContext):
    """Main entry point - LiveKit calls this when a user connects"""
    logger.info(f"User connected to room: {ctx.room.name}")
    
    # Create and start the agent session
    session = AgentSession(
        turn_detection="stt",
        min_endpointing_delay=0.07
    )
    await session.start(
        agent=VoiceAgent(),
        room=ctx.room
    )

if __name__ == "__main__":
    # Run the agent
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
