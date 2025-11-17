"""
Invoice Agent
Handles invoice CRUD operations via built-in Supabase tools using @tool decorators.
"""

from strands import Agent, tool
import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from ..config.conversation_config import ConversationConfig, log_conversation_config
from ..config.config import create_bedrock_model
from ..utils.prompt_consent import get_consent_instructions
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class InvoiceAgent(Agent):
    """
    Specialized agent for CRUD operations on the Supabase database regarding Invoice information.
    """

    def __init__(self, config=None):
        
        if config is None:
            raise RuntimeError("No config provided")
        
        # initialize supabase connection
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set")
            
        self.supabase_client : Client = create_client(
            url,
            key,
            options=ClientOptions(
                postgrest_client_timeout=10,
                storage_client_timeout=10,
                schema="api",
            )
        )
        logger.debug(f"supabase_client: {self.supabase_client}")
        
        # Create properly configured Bedrock model
        bedrock_model = create_bedrock_model(config)

        # Create conversation manager for invoice operations
        conversation_manager = ConversationConfig.create_conversation_manager("invoiceManager")

        # Initialize Strands Agent with system prompt and tools
        system_prompt = self._get_instructions()
        super().__init__(
            model=bedrock_model,
            system_prompt=system_prompt,
            tools=[
                self.list_all_invoices, 
                self.get_invoice_by_number, 
                self.get_invoices_by_client, 
                self.update_invoice_status,
                self.create_invoice,
                self.update_invoice,
                self.delete_invoice
            ],
            conversation_manager=conversation_manager,
        )

        # Log configuration
        logger.info("InvoiceAgent initialized with built-in Supabase tools")
        log_conversation_config("InvoiceAgent", conversation_manager)

    @tool
    def list_all_invoices(self) -> str:
        """List all invoices in the database.
        
        Args:
            None
        """
        try:
            response = (
                self.supabase_client
                .table("invoices")
                .select("*")
                .execute()
            )
            logger.debug(f"list_all_invoices response: {response}")
            return str(response.data)
            
        except Exception as e:
            logger.error(f"Error listing invoices: {e}")
            return f"Error retrieving invoices: {str(e)}"

    @tool
    def get_invoice_by_number(self, invoice_number: str) -> str:
        """Get specific invoice by invoice number.
        
        Args:
            invoice_number (str): The unique invoice number to search for (e.g., 'INV-001')
        """
        try:
            response = (
                self.supabase_client.table("invoices")
                .select("*")
                .eq("invoice_number", invoice_number)
                .execute()
            )
            if response.data:
                invoice = response.data[0]
                return f"Invoice {invoice_number}: {invoice.get('client_name')}, ${invoice.get('total_amount')}, Balance: ${invoice.get('balance_due')}, Status: {invoice.get('status')}"
            else:
                return f"Invoice {invoice_number} not found"
            
        except Exception as e:
            logger.error(f"Error getting invoice {invoice_number}: {e}")
            return f"Error retrieving invoice: {str(e)}"

    @tool
    def get_invoices_by_client(self, client_name: str) -> str:
        """Get all invoices for a specific client.
        
        Args:
            client_name (str): The name of the client to search invoices for (e.g., 'John Smith')
        """
        try:
            response = self.supabase_client.table('invoices').select('*').eq('client_name', client_name).execute()
            return  str(response.data)
        except Exception as e:
            logger.error(f"Error getting invoices for client {client_name}: {e}")
            return f"Error retrieving client invoices: {str(e)}"

    @tool
    def update_invoice_status(self, invoice_number: str, new_status: str) -> str:
        """Update the status of an invoice.
        
        Args:
            invoice_number (str): The unique invoice number to update (e.g., 'INV-001')
            new_status (str): The new status value. Valid options: 'draft', 'sent', 'viewed', 'partial', 'paid', 'overdue', 'cancelled'
        """
        valid_statuses = ['draft', 'sent', 'viewed', 'partial', 'paid', 'overdue', 'cancelled']
        if new_status.lower() not in valid_statuses:
            return f"Invalid status. Valid statuses: {', '.join(valid_statuses)}"
        
        try:
            response = (
                self.supabase_client.table("invoices")
                .update({"status": new_status.lower()})
                .eq("invoice_number", invoice_number)
                .execute()
            )
            if response.data:
                return f"Invoice {invoice_number} status updated to {new_status}"
            else:
                return f"Invoice {invoice_number} not found"
            
        except Exception as e:
            logger.error(f"Error updating invoice {invoice_number}: {e}")
            return f"Error updating invoice: {str(e)}"

    @tool
    def create_invoice(self, client_name: str, client_email: str, total_amount: float, invoice_number: str = None, due_date: str = None) -> str:
        """Create a new invoice.
        
        Args:
            client_name (str): The name of the client for the invoice (e.g., 'John Smith')
            client_email (str): The email address of the client (e.g., 'john@example.com')
            total_amount (float): The total amount for the invoice in dollars (e.g., 2500.00)
            invoice_number (str, optional): Custom invoice number. If not provided, will be auto-generated
            due_date (str, optional): Due date in YYYY-MM-DD format. If not provided, will be set to 30 days from today
        """
        try:
            from datetime import datetime, timedelta
            
            # Auto-calculate due_date if not provided (30 days from today)
            if due_date is None:
                due_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            
            invoice_data = {
                "client_name": client_name,
                "client_email": client_email,
                "total_amount": total_amount,
                "status": "draft",
                "due_date": due_date
            }
            if invoice_number:
                invoice_data["invoice_number"] = invoice_number
                
            response = (
                self.supabase_client.table("invoices")
                .insert(invoice_data)
                .execute()
            )
            if response.data:
                created_invoice = response.data[0]
                return f"Invoice created: {created_invoice.get('invoice_number', 'N/A')} for {client_name}, Amount: ${total_amount}"
            else:
                return "Failed to create invoice"
                
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            return f"Error creating invoice: {str(e)}"

    @tool
    def update_invoice(self, invoice_number: str, **kwargs) -> str:
        """Update invoice fields. Available fields: client_name, client_email, total_amount, balance_due, status, notes.
        
        Args:
            invoice_number (str): The unique invoice number to update (e.g., 'INV-001')
            **kwargs: Keyword arguments for fields to update. Valid fields include:
                - client_name (str): Update the client name
                - client_email (str): Update the client email address
                - total_amount (float): Update the total amount
                - balance_due (float): Update the balance due
                - status (str): Update the invoice status
                - notes (str): Update invoice notes
                - due_date (str): Update the due date
        """
        try:
            # Filter valid fields
            valid_fields = ['client_name', 'client_email', 'total_amount', 'balance_due', 'status', 'notes', 'due_date']
            update_data = {k: v for k, v in kwargs.items() if k in valid_fields and v is not None}
            
            if not update_data:
                return "No valid fields provided for update"
                
            response = (
                self.supabase_client.table("invoices")
                .update(update_data)
                .eq("invoice_number", invoice_number)
                .execute()
            )
            if response.data:
                return f"Invoice {invoice_number} updated successfully"
            else:
                return f"Invoice {invoice_number} not found"
                
        except Exception as e:
            logger.error(f"Error updating invoice {invoice_number}: {e}")
            return f"Error updating invoice: {str(e)}"

    @tool
    def delete_invoice(self, invoice_number: str) -> str:
        """Delete an invoice by invoice number.
        
        Args:
            invoice_number (str): The unique invoice number to delete (e.g., 'INV-001')
        """
        try:
            response = (
                self.supabase_client.table("invoices")
                .delete()
                .eq("invoice_number", invoice_number)
                .execute()
            )
            if response.data:
                return f"Invoice {invoice_number} deleted successfully"
            else:
                return f"Invoice {invoice_number} not found"
                
        except Exception as e:
            logger.error(f"Error deleting invoice {invoice_number}: {e}")
            return f"Error deleting invoice: {str(e)}"

    def _get_instructions(self) -> str:
        """Get the instructions for the InvoiceAgent."""
        base_instructions = """
        You are an Invoice Management Agent that ONLY performs CRUD operations on the invoice table.

        **Available Tools:**
        - list_all_invoices(): Get all invoices in the database
        - get_invoice_by_number(invoice_number): Get specific invoice details
        - get_invoices_by_client(client_name): Get all invoices for a client
        - update_invoice_status(invoice_number, new_status): Update invoice status
        - create_invoice(client_name, client_email, total_amount, invoice_number): Create new invoice
        - update_invoice(invoice_number, **kwargs): Update invoice fields
        - delete_invoice(invoice_number): Delete an invoice

        **Strict Limitations:**
        - ONLY perform CRUD operations on the invoices table
        - NO access to other tables (contacts, projects, etc.)
        - NO other operations beyond Create, Read, Update, Delete

        **Response Format:**
        - Voice-optimized: under 800 characters
        - Include: invoice_number, client_name, total_amount, balance_due, status

        **Status Values:** draft, sent, viewed, partial, paid, overdue, cancelled

        Handle ONLY invoice CRUD operations as directed by orchestrator."""
        
        consent_instructions = get_consent_instructions()
        return base_instructions + "\n\n" + consent_instructions
