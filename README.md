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

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/health-line-assistant.git
cd health-line-assistant
```

2. **Create a virtual environment**
```bash
python -m venv .venv
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -e .
# or using uv
uv pip install -e .
```

4. **Configure environment variables**
Create a `.env.local` file in the root directory:
```env
OPENAI_API_KEY=your_openai_key
DEEPGRAM_API_KEY=your_deepgram_key
ELEVENLABS_API_KEY=your_elevenlabs_key
LIVEKIT_URL=your_livekit_server_url
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
```

## Usage 📞

### Starting the Agent

```bash
python agent/agent.py
```

The agent will start listening for incoming RTC (Real-Time Communication) sessions from:
- Phone calls (via SIP)
- Web clients
- LiveKit clients

### Making a Call

The assistant will greet the caller and help them with:
1. **Appointments**: "I'd like to book an appointment"
2. **Prescriptions**: "I need a medicine refill"
3. **Recommendations**: "What doctor should I see for [symptom]?"
4. **General Help**: "I need assistance with..."

## Key Modules 🔧

### `agent.py`
Main entry point that:
- Initializes the voice assistant
- Configures STT, TTS, and LLM settings
- Sets up audio processing (VAD, noise cancellation)
- Manages incoming sessions

### `prompt.py`
Contains system instructions for the LLM:
- Speaking style guidelines
- Medical safety rules and restrictions
- Appointment booking procedures
- Prescription handling protocols
- Symptom-to-specialist mapping

### `functions.py`
Tool functions available to the assistant:
- `save_appointment()` - Store appointment bookings
- `save_medicine_refill_order()` - Process prescription refills
- `get_doctors_list()` - Retrieve available doctors
- `transfer_to_human()` - Transfer to human agent
- `end_call()` - Gracefully end conversation

### `doctors.json`
Database containing:
- Available doctors and specialists
- Their specialties and availability
- Contact information

## Data Files 📊

- **appointments.jsonl**: Line-delimited JSON file storing appointment records
- **prescriptions.jsonl**: Line-delimited JSON file storing prescription requests

## Environment Variables 🔐

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENAI_API_KEY` | OpenAI API key for GPT-4.1 | Yes |
| `DEEPGRAM_API_KEY` | Deepgram API key for speech recognition | Yes |
| `ELEVENLABS_API_KEY` | ElevenLabs API key for voice synthesis | Yes |
| `LIVEKIT_URL` | LiveKit server URL | Yes |
| `LIVEKIT_API_KEY` | LiveKit API key | Yes |
| `LIVEKIT_API_SECRET` | LiveKit API secret | Yes |

**⚠️ Never commit `.env.local` to version control!**

## Medical Safety Guidelines ⚕️

This assistant follows strict medical safety protocols:
- ✅ Provides general wellness advice
- ✅ Suggests appropriate specialists based on symptoms
- ✅ Helps with appointment scheduling
- ❌ Does NOT provide medical diagnosis
- ❌ Does NOT replace professional medical advice
- ❌ Does NOT prescribe medications

Always transfers to human agents for complex medical questions.

## Development 💻

### Code Structure
- Audio input → Deepgram STT → LLM Processing → ElevenLabs TTS → Audio output
- All audio processing includes noise cancellation and turn detection

### Extending Functionality
To add new tools or capabilities:
1. Define the function in `functions.py`
2. Add it to the `tools` list in `agent.py`
3. Update the LLM prompt in `prompt.py` to guide usage

## Troubleshooting 🐛

**Issue**: No audio input detected
- Check LiveKit connection
- Verify microphone permissions
- Ensure VAD model is loaded

**Issue**: Poor speech recognition
- Check Deepgram API key
- Verify good audio quality
- Ensure noise cancellation is enabled

**Issue**: Slow responses
- Check OpenAI API status
- Verify network connectivity
- Review API rate limits

## Contributing 🤝

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see LICENSE file for details.

## Contact & Support 💬

For questions or support:
- Create an issue on GitHub
- Contact the development team

## Acknowledgments 🙏

- [LiveKit](https://livekit.io/) - Real-time communication platform
- [OpenAI](https://openai.com/) - Language model API
- [Deepgram](https://deepgram.com/) - Speech recognition
- [ElevenLabs](https://elevenlabs.io/) - Text-to-speech

---

**Last Updated**: December 30, 2025
