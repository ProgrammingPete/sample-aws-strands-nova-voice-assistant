---
inclusion: always
---

# Project Structure

## Root Directory

```
├── backend/                    # Python backend application
├── frontend/                   # React web interface
├── test/                       # Test files
├── diagrams/                   # Architecture diagrams
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Python project configuration
├── run_backend.sh             # Backend startup script
├── run_frontend.sh            # Frontend startup script
├── .env                       # Environment variables (not in git)
└── .env.example               # Environment variable template
```

## Backend Structure

```
backend/
├── src/voice_based_aws_agent/
│   ├── agents/                # Multi-agent system
│   │   ├── orchestrator.py    # Central agent coordinator
│   │   ├── supervisor_agent.py # Query routing agent (pure router)
│   │   ├── ec2_agent.py       # EC2 operations specialist
│   │   ├── aws_researcher_agent.py # AWS documentation research
│   │   ├── invoice_agent.py   # Invoice processing
│   │   └── old_agents/        # Deprecated agents (backup_agent.py, ssm_agent.py)
│   ├── config/                # Configuration management
│   │   ├── config.py          # Bedrock model configuration
│   │   ├── conversation_config.py # Conversation management
│   │   └── tool_config.py     # Tool configuration
│   ├── utils/                 # Utility modules
│   │   ├── aws_auth.py        # AWS authentication
│   │   ├── prompt_consent.py  # Tool consent handling
│   │   └── voice_integration/ # Nova Sonic integration
│   │       ├── server.py      # WebSocket server
│   │       ├── s2s_session_manager.py # Stream management
│   │       ├── s2s_events.py  # Event handling
│   │       └── supervisor_agent_integration.py # Agent bridge
│   └── main.py                # Application entry point
└── tools/                     # Strands tools
    └── supervisor_tool.py     # Supervisor agent tool integration
```

## Frontend Structure

```
frontend/
├── src/
│   ├── components/            # React components
│   │   └── EventDisplay.js    # Event display component
│   ├── helper/                # Utility functions
│   │   ├── audioHelper.js     # Audio processing
│   │   ├── audioPlayer.js     # Audio playback
│   │   ├── audioPlayerProcessor.worklet.js # Audio worklet
│   │   └── s2sEvents.js       # Speech-to-speech events
│   ├── App.js                 # Main React application
│   ├── VoiceAgent.js          # Voice interface component
│   ├── App.css                # Main styles
│   ├── VoiceAgent.css         # Voice interface styles
│   └── index.js               # React entry point
├── public/
│   ├── index.html             # HTML template
│   ├── manifest.json          # PWA manifest
│   └── audioPlayerProcessor.worklet.js # Audio worklet (public)
└── package.json               # Node.js dependencies
```

## Key Architectural Patterns

### Multi-Agent System

- **Orchestrator**: Coordinates agent initialization and lifecycle
- **Supervisor Agent**: Pure router with no tools, routes queries to specialized agents
- **Specialized Agents**: Domain-specific agents (EC2Agent, AWSResearcherAgent, etc.)
- Each agent has its own conversation manager with sliding window context

### Voice Integration

- WebSocket server handles real-time bidirectional communication
- Session manager coordinates Nova Sonic streams
- Agent integration bridges voice input/output with agent responses

### Configuration Management

- Centralized config for Bedrock model creation
- Conversation config manages context windows per agent
- Tool config handles AWS service integrations

## File Naming Conventions

- Python files: snake_case (e.g., `supervisor_agent.py`)
- React components: PascalCase (e.g., `VoiceAgent.js`)
- CSS files: match component names (e.g., `VoiceAgent.css`)
- Config files: descriptive names with `_config.py` suffix

## Import Patterns

- Backend uses relative imports within the package (e.g., `from ..config.config import`)
- Frontend uses relative imports for local modules (e.g., `./helper/audioHelper`)
- AWS SDK imports use boto3 for service clients
- Strands framework imported as `from strands import Agent`
