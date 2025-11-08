"""
Supervisor Agent - Pure Router
Routes user queries to appropriate specialized agents without any tools or reasoning.
"""

from strands import Agent
from typing import Dict, Any
from ..config.conversation_config import ConversationConfig, log_conversation_config
from ..config.config import create_bedrock_model
import logging

logger = logging.getLogger(__name__)


class SupervisorAgent(Agent):
    """
    Supervisor Agent that acts as a pure router.
    No tools, no reasoning - just routing based on query type.
    """

    def __init__(self, specialized_agents: Dict[str, Agent], config=None):
        """
        Initialize supervisor with references to specialized agents.

        Args:
            specialized_agents: Dictionary mapping agent names to agent instances
            config: AgentConfig instance for AWS profile and region settings
        """
        
        if config is None:
            raise RuntimeError("No config provided")
        
        # Create properly configured Bedrock model with specified profile
        bedrock_model = create_bedrock_model(config)

        # Create conversation manager for supervisor (smaller window since it just routes)
        conversation_manager = ConversationConfig.create_conversation_manager(
            "supervisor"
        )

        # Initialize Strands Agent with system prompt but no tools
        system_prompt = self._get_routing_instructions()
        super().__init__(
            model=bedrock_model,
            system_prompt=system_prompt,
            tools=[],  # No tools for pure router
            conversation_manager=conversation_manager,
        )

        self.specialized_agents = specialized_agents

        # Log configuration
        logger.info(
            "SupervisorAgent initialized with BedrockModel (configured profile, us-east-1, Nova Lite)"
        )
        log_conversation_config("SupervisorAgent", conversation_manager)
        logger.info(
            f"Supervisor initialized with agents: {list(specialized_agents.keys())} and conversation management"
        )

    def _get_routing_instructions(self) -> str:
        """Get the routing instructions for the supervisor."""
        return """
You are a Supervisor Agent that acts as a pure router for customer's queries. 

1. First, validate that the query is realted to programming
2. If non-programming, politely redirect to AWS topics
3. Route the query to the appropriate agent
4. Return the agent's response

AWS QUERY VALIDATION:
- ONLY handle queries about AWS services, operations, infrastructure, or documentation and research
- Reject queries about:  personal topics, entertainment, finance

ROUTING RULES (for valid AWS queries):
- AWS lambda documentation queries and general AWS questions -> AWSResearcherAgent
- AWS EC2-related queries (instances, status, management) → EC2Agent
- When asked to perform research on AWS → aws_researcher
- General AWS queries that don't fit above → AWSResearcherAgent (default)

CONVERSATION CONTEXT:
- Remember which agents handled recent queries
- Consider conversation flow when routing follow-up questions
- Route follow-up questions to the same agent when contextually relevant

DO NOT:
- Use any tools yourself
- Make AWS API calls

ALWAYS:
- Pass the original user query unchanged to agents
- Return the specialized agent's response
- Consider conversation history for routing decisions
"""

    async def route_query(self, query: str) -> str:
        """
        Route a query to the appropriate specialized agent.

        Args:
            query: User query to route

        Returns:
            Response from the specialized agent
        """
        logger.info(f"Routing query: {query}")

        # Determine which agent to route to
        agent_name = self._determine_agent(query)

        if agent_name not in self.specialized_agents:
            logger.error(f"Agent {agent_name} not found in specialized agents")
            return f"Error: Unable to route query - {agent_name} not available"

        # Route to specialized agent
        specialized_agent = self.specialized_agents[agent_name]
        logger.info(f"Routing to {agent_name}")

        try:
            # Use the Strands Agent's direct call method
            response = specialized_agent(query)
            logger.info(f"Received response from {agent_name}")
            return str(response)

        except Exception as e:
            logger.error(f"Error from {agent_name}: {str(e)}")
            return f"Error: {agent_name} encountered an issue: {str(e)}"

    def _determine_agent(self, query: str) -> str:
        """
        Determine which agent should handle the query based on keywords.

        Args:
            query: User query

        Returns:
            Name of the agent to route to
        """
        query_lower = query.lower()

        # SSM keywords
        # ssm_keywords = [
        #     "ssm",
        #     "systems manager",
        #     "patch",
        #     "command",
        #     "document",
        #     "run command",
        #     "session manager",
        #     "parameter store",
        #     "cloudwatch agent",
        #     "install",
        #     "configure",
        # ]

        # # Backup keywords
        # backup_keywords = [
        #     "backup",
        #     "restore",
        #     "vault",
        #     "backup plan",
        #     "backup job",
        #     "recovery",
        #     "snapshot",
        # ]

        # EC2 keywords (and default)
        ec2_keywords = [
            "ec2",
            "instance",
            "server",
            "vm",
            "virtual machine",
            "compute",
            "ami",
            "security group",
            "vpc",
        ]
        
        lambda_keywords = [
            "lambda",
        ]

        # Check for SSM
        # if any(keyword in query_lower for keyword in ssm_keywords):
        #     logger.info("SSM query detected, routing to SSMAgent")
        #     return "SSMAgent"

        # Check for Backup
        # if any(keyword in query_lower for keyword in backup_keywords):
        #     logger.info("Backup query detected, routing to BackupAgent")
        #     return "BackupAgent"
        
        if any(keyword in query_lower for keyword in lambda_keywords):
            logger.info("Lambda query detected, routing to AWSResearcherAgent")
            return "AWSResearcherAgent"
        
        #         # Check for EC2
        if any(keyword in query_lower for keyword in ec2_keywords):
            return "EC2Agent"

        # Default to EC2Agent for general queries
        logger.info("Defaulting to AWSResearcherAgent for general query")
        return "AWSResearcherAgent"
