# Health Line Assistant 🏥

A voice-based health assistant powered by AI that helps patients book appointments, manage prescriptions, and get general health guidance through natural voice conversations.

## Features ✨

- **Voice Conversations**: Interact naturally with an AI health assistant using voice
- **Appointment Booking**: Schedule doctor appointments seamlessly
- **Prescription Management**: Request medicine refills and prescription renewals
- **Doctor Recommendations**: Get suggestions for appropriate specialists based on symptoms
- **Multi-Language Support**: Uses multilingual turn detection for diverse users
- **Real-time Audio Processing**: Advanced noise cancellation and voice activity detection
- **Medical-Grade STT**: Deepgram Nova-3 medical speech-to-text model
- **Human Handoff**: Seamlessly transfer to human agents when needed

## Technology Stack 🛠️

- **Framework**: [LiveKit Agents](https://docs.livekit.io/agents/) - Voice AI agents framework
- **LLM**: OpenAI GPT-4.1
- **Speech-to-Text**: Deepgram Nova-3 Medical
- **Text-to-Speech**: ElevenLabs Turbo V2.5
- **Voice Activity Detection**: Silero VAD
- **Language**: Python 3.10+
- **Audio Enhancement**: Noise cancellation, multilingual turn detection

## Project Structure 📁

```
health-line-assistant/
├── agent/
│   ├── agent.py              # Main agent entry point
│   ├── prompt.py             # LLM system instructions and prompts
│   ├── functions.py          # Tool functions for appointments, prescriptions, etc.
│   ├── doctors.json          # Available doctors database
│   └── __pycache__/
├── KMS/
│   └── logs/                 # Application logs
├── appointments.jsonl        # Stored appointment records
├── prescriptions.jsonl       # Stored prescription records
├── pyproject.toml            # Python dependencies and project metadata
├── .env.local               # Environment variables (not committed)
├── .gitignore               # Git ignore rules
├── README.md                # This file
├── next-env.d.ts            # TypeScript definitions
├── package-lock.json        # Node.js dependencies
└── uv.lock                  # uv package manager lock file
```

## Setup Instructions 🚀

### Prerequisites
- Python 3.10 or higher
- pip or uv package manager
- Environment variables configured


## Development 💻

### Code Structure
- Audio input → Deepgram STT → LLM Processing → ElevenLabs TTS → Audio output
- All audio processing includes noise cancellation and turn detection

### Extending Functionality
To add new tools or capabilities:
1. Define the function in `functions.py`
2. Add it to the `tools` list in `agent.py`
3. Update the LLM prompt in `prompt.py` to guide usage

