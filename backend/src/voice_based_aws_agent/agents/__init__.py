"""
Multi-Agent Orchestration System for Voice-based AWS Agent

This package contains the multi-agent system with:
- SupervisorAgent: Pure router that forwards queries to specialized agents
- EC2Agent: Handles EC2-related operations
- SSMAgent: Handles Systems Manager operations (DISABLED)
- BackupAgent: Handles AWS Backup operations (DISABLED)
- AWSResearcherAgent: Does research task against the AWS online documentation. Handles all queries
- AgentOrchestrator: Manages the entire multi-agent system
"""

from .supervisor_agent import SupervisorAgent
from .ec2_agent import EC2Agent
# from .old_agents.ssm_agent import SSMAgent
# from .old_agents.backup_agent import BackupAgent
from .orchestrator import AgentOrchestrator
from .aws_researcher_agent import AWSResearcherAgent

__all__ = [
    "SupervisorAgent",
    "EC2Agent", 
    # "SSMAgent",
    # "BackupAgent",
    "AgentOrchestrator",
    "AWSResearcherAgent"
]
