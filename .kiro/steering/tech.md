---
inclusion: always
---

# Technology Stack

## Backend

- **Language**: Python 3.12+
- **Framework**: AWS Strands framework for multi-agent orchestration
- **Package Manager**: pip with requirements.txt (standard Python dependency management)
- **Key Libraries**:
  - `strands-agents` - Multi-agent framework
  - `strands-agents-tools` - Agent tooling
  - `boto3` - AWS SDK for Python
  - `websockets==10.4` - WebSocket server implementation
  - `pyaudio` - Audio processing
  - `python-dotenv` - Environment variable management
  - `asyncio` - Asynchronous operations
  - `supabase` - Database client

## Frontend

- **Framework**: React 18.2
- **Build Tool**: react-scripts (Create React App)
- **UI Library**: AWS Cloudscape Design Components
- **Package Manager**: npm

## AWS Services

- **AI Models**: AWS Bedrock Nova Lite (for all agents)
- **Voice Processing**: Amazon Nova Sonic (speech-to-text and text-to-speech)
- **AWS Services**: EC2, SSM, AWS Backup, Lambda (via boto3)

## Authentication

- **Nova Sonic**: Requires AWS credentials as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_DEFAULT_REGION)
- **Other AWS Services**: Uses boto3 with AWS profiles

## Common Commands

### Backend

```bash
# Setup virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run backend server (default port 8080)
./run_backend.sh

# Run with custom parameters
./run_backend.sh --profile <profile> --region <region> --voice matthew --port 8080
```

### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Run development server (port 3000)
./run_frontend.sh
# or
cd frontend && npm start

# Build for production
npm run build

# Run tests
npm test
```

### Environment Setup

```bash
# Set AWS credentials for Nova Sonic (required)
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_SESSION_TOKEN=<your-session-token>  # if using temporary credentials
export AWS_DEFAULT_REGION=<your-region>

# Configure AWS CLI profile for other services
aws configure --profile <your-profile-name>
```

## Development Notes

- Default backend port is 8080 (changed from 80 to avoid requiring admin privileges)
- Frontend expects WebSocket connection at ws://localhost:8080
- Voice responses are truncated to 800 characters for optimal voice experience
- Tool consent is bypassed via BYPASS_TOOL_CONSENT environment variable
