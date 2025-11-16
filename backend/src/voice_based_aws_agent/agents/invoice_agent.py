"""
Invoice Agent
Handles invoice CRUD operations via PostgreSQL MCP server.
"""

from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import StdioServerParameters, stdio_client
from ..config.conversation_config import ConversationConfig, log_conversation_config
from ..config.config import create_bedrock_model
from ..utils.prompt_consent import get_consent_instructions
import logging
import os

logger = logging.getLogger(__name__)


class InvoiceAgent(Agent):
    """
    Specialized agent for CRUD operations on the PostgreSQL database regarding Invoice information.
    """

    def __init__(self, config=None):
        
        if config is None:
            raise RuntimeError("No config provided")
        
        # Get Supabase password from environment
        supabase_password = os.getenv('SUPABASE_PASSWORD')
        if not supabase_password:
            raise RuntimeError("SUPABASE_PASSWORD environment variable not set")
        
        # Store MCP PostgreSQL client for Supabase (Transaction mode)
        connection_string = f"postgresql://postgres.emdlwkjdqbsbeeamgffq:{supabase_password}@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
        
        self.postgres_mcp_client = MCPClient(
            lambda: stdio_client(
                StdioServerParameters(
                    command="uvx",
                    args=["mcp-server-postgres", connection_string]
                )
            )
        )
        
        # Create properly configured Bedrock model
        bedrock_model = create_bedrock_model(config)

        # Create conversation manager for research operations
        conversation_manager = ConversationConfig.create_conversation_manager("invoiceManager")

        # Initialize Strands Agent with system prompt and conversation management
        system_prompt = self._get_instructions()
        super().__init__(
            model=bedrock_model,
            system_prompt=system_prompt,
            tools=[self.postgres_mcp_client],
            conversation_manager=conversation_manager,
        )

        # Log configuration
        logger.info("InvoiceAgent initialized with PostgreSQL MCP client")
        log_conversation_config("InvoiceAgent", conversation_manager)

    def _get_instructions(self) -> str:
        """Get the instructions for the InvoiceAgent."""
        base_instructions = """You are an Invoice Management Agent that receives requests from the orchestrator agent.

**Access Restrictions:**
- ONLY access the invoices table in Supabase
- NO access to other tables (contacts, projects, etc.)
- Work with data provided by orchestrator agent

**CRUD Operations on invoices table:**
- CREATE: Insert new invoices with required fields
- READ: Query by invoice_number, client_name, status, date ranges
- UPDATE: Modify amounts, dates, status, payment info
- DELETE: Remove invoices (except paid ones)

**Invoice Table Schema:**
- id (UUID), invoice_number (TEXT, unique), client_name (TEXT)
- issue_date, due_date, paid_date (DATE)
- subtotal, tax_amount, total_amount, amount_paid (DECIMAL)
- balance_due (auto-calculated: total_amount - amount_paid)
- line_items (JSONB), status (TEXT), notes (TEXT)

**Status Values:** draft, sent, viewed, partial, paid, overdue, cancelled

**Response Format:**
- Voice-optimized: under 800 characters
- Include: invoice_number, client_name, total_amount, balance_due, status

**SQL Guidelines:**
- Use parameterized queries via MCP tools
- Only query invoices table: SELECT * FROM invoices WHERE...
- Handle JSONB line_items with operators
- No JOINs with other tables

Handle only invoice CRUD operations as directed by orchestrator."""
        
        consent_instructions = get_consent_instructions()
        return base_instructions + "\n\n" + consent_instructions
