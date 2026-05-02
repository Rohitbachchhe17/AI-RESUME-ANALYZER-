import os
from dotenv import load_dotenv
from loguru import logger
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.services.openai.llm import OpenAILLMService
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.daily.transport import DailyParams

load_dotenv(override=True)

async def bot(runner_args: RunnerArguments):
    """Main bot entry point."""
    
    # Create transport (supports both Daily and WebRTC)
    transport = await create_transport(
        runner_args,
        {
            "daily": lambda: DailyParams(audio_in_enabled=True, audio_out_enabled=True),
            "webrtc": lambda: TransportParams(
                audio_in_enabled=True, audio_out_enabled=True
            ),
        },
    )

    # Initialize AI services using Sarvam for Audio and OpenRouter for LLM
    stt = SarvamSTTService(api_key=os.getenv("SARVAM_API_KEY"))
    tts = SarvamTTSService(api_key=os.getenv("SARVAM_API_KEY"))
    
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model_name = "openai/gpt-4o-mini" if "openrouter" in base_url else "gpt-4o-mini"
    
    llm = OpenAILLMService(
        api_key=os.getenv("OPENAI_API_KEY"), 
        model=model_name,
        base_url=base_url
    )

    # Set up highly professional conversation context
    messages = [
        {
            "role": "system",
            "content": "You are an elite, highly professional AI Career Coach. You help users analyze their resumes, predict job fit, and provide advanced career strategies. Keep your responses highly accurate, helpful, and concise.",
        },
    ]
    context = LLMContext(messages)
    context_aggregator = LLMContextAggregatorPair(context)

    # Build pipeline
    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            context_aggregator.user(),
            llm,
            tts,
            transport.output(),
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(pipeline)

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Client connected")
        messages.append(
            {"role": "system", "content": "Say hello, introduce yourself as the AI Career Coach, and ask the user how you can help them with their resume today."}
        )
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    runner = PipelineRunner(handle_sigint=runner_args.handle_sigint)
    await runner.run(task)

if __name__ == "__main__":
    from pipecat.runner.run import main
    main()
