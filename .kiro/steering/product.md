---
inclusion: always
---

# AWS Strands Nova Voice Assistant

A voice-based AI assistant that uses AWS Strands for multi-agent collaboration to interact with AWS services. The system features real-time voice interaction through Amazon Nova Sonic and intelligent routing between specialized AWS agents.

## Core Capabilities

- Real-time voice input/output using Amazon Nova Sonic
- Multi-agent architecture with supervisor routing to specialized agents
- AWS service integration (EC2, SSM, AWS Backup, Lambda documentation)
- WebSocket-based communication between React frontend and Python backend
- Professional UI using AWS Cloudscape Design components

## Key Design Principles

- Simple session management without complex recovery mechanisms
- User-controlled recovery (manual restart on errors rather than automatic recovery)
- Voice-optimized responses (truncated to 800 characters for better voice experience)
- Single tool architecture: supervisor agent routes to specialized agents
- Straightforward error handling that asks users to restart rather than automatic recovery

## Target Use Cases

- Voice-driven AWS infrastructure management
- EC2 instance operations (start, stop, status checks)
- AWS documentation research and queries
- Systems Manager operations
- Backup management and monitoring
