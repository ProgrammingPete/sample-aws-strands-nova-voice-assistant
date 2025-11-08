"""
EC2 Specialized Agent
Handles all EC2-related queries with full reasoning and AWS API access.
"""

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client
from ..config.conversation_config import ConversationConfig, log_conversation_config
from ..config.config import create_bedrock_model
from ..utils.prompt_consent import get_consent_instructions
import logging

logger = logging.getLogger(__name__)


class AWSResearcherAgent(Agent):
    """
    Specialized agent for Reserach AWS Documentation.
    Has access to AWS documentation MCP server. 
    """

    def __init__(self, config=None):
        
        if config is None:
            raise RuntimeError("No config provided")
        
        
        aws_documentation_mcp_server = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=["awslabs.aws-documentation-mcp-server@latest"]
                )
            )
        )
        with aws_documentation_mcp_server:
            print("Connected to mcp server: aws-documentation-mcp-server")
            tools = aws_documentation_mcp_server.list_tools_sync()
            
            # Create properly configured Bedrock model
            bedrock_model = create_bedrock_model(config)

            # Create conversation manager for EC2 operations
            conversation_manager = ConversationConfig.create_conversation_manager("researcher")

            # Initialize Strands Agent with system prompt, tools, and conversation management
            system_prompt = self._get_instructions()
            super().__init__(
                model=bedrock_model,
                system_prompt=system_prompt,
                tools=tools,
                conversation_manager=conversation_manager,
            )

            # Log configuration
            logger.info(
                "AWSResearcherAgent initialized with BedrockModel and consent-aware prompts (configured profile, us-east-1, Nova Lite)"
            )
            log_conversation_config("AWSResearcherAgent", conversation_manager)

    def _get_instructions(self) -> str:
        """Get the instructions for the AWSResearcherAgent."""
        base_instructions = """
            You are a thorough AWS researcher specialized in finding accurate information online. 
            You have the capability to directly search or browse through AWS documentation. Using the MCP tools
            For each question:
            1. Determine what information you need
            2. Search the AWS Documentation for reliable information
            3. Extract key information and cite your sources
            4. Store important findings in memory for future reference
            5. Synthesize what you've found into a clear, comprehensive answer

            When researching, focus only on AWS documentation. Always provide citations for the information you find. 
"""
        
        # Add consent instructions
        consent_instructions = get_consent_instructions()
        
        return base_instructions + "\n\n" + consent_instructions
