from dotenv import load_dotenv
import os

from livekit import agents, rtc
from livekit.agents import AgentServer, AgentSession, Agent, room_io

from livekit.plugins import noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Imports from your project modules
from prompt import GENERAL_INSTRUCTIONS, SESSION_GREETING
from functions import transfer_to_human, end_call, save_appointment, save_medicine_refill_order, get_doctors_list


load_dotenv(".env.local")


class VoiceAssistant(Agent):
    """
    Core Agent class. Loads instructions and function-calling map.
    """

    def __init__(self) -> None:
        super().__init__(
            instructions=GENERAL_INSTRUCTIONS,
            tools = [transfer_to_human, end_call, save_appointment, save_medicine_refill_order, get_doctors_list]
        )


async def healthline_agent(ctx: agents.JobContext):
    """
    Entry point for every new incoming RTC session (SIP/Phone/Web).
    Defines STT, TTS, LLM, VAD, turn detection, noise cancellation settings.
    """

    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)

    print("==================Agent Starting============")

    # Create session
    session = AgentSession(
        stt="deepgram/nova-3-medical:en",
        llm="openai/gpt-4.1",
        tts="elevenlabs/eleven_turbo_v2_5:cgSgspJ2msm6clMCkdW9",

        # VAD + Turn Detection
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    # Start the agent with audio config
    await session.start(
        room=ctx.room,
        agent=VoiceAssistant(),
        room_options=room_io.RoomOptions(
            audio_input=room_io.AudioInputOptions(
                noise_cancellation=lambda params:
                    noise_cancellation.BVCTelephony()
                    if params.participant.kind == rtc.ParticipantKind.PARTICIPANT_KIND_SIP
                    else noise_cancellation.BVC()
            ),
        ),
    )

    # Initial greeting instruction
    await session.generate_reply(instructions=SESSION_GREETING)


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=healthline_agent,
            agent_name="Health-Line-Assistant"
        )
    )
