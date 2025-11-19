#!/usr/bin/env python3
"""
Property-based test for invoice retrieval consistency
Feature: invoice-agent, Property 1: Invoice retrieval consistency
Validates: Requirements 2.1, 2.2
"""

import sys
import os
from datetime import datetime, timedelta

# Add the backend src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend', 'src'))

from hypothesis import given, strategies as st, settings
from dotenv import load_dotenv
from voice_based_aws_agent.agents.invoice_agent import InvoiceAgent
from voice_based_aws_agent.config.config import AgentConfig

# Load environment variables
load_dotenv()

# Initialize agent once for all tests
config = AgentConfig()
agent = InvoiceAgent(config)


def extract_invoice_number(response: str) -> str:
    """Extract invoice number from create response"""
    # Response format: "Invoice created: INV-XXX for ..."
    if "Invoice created:" in response:
        parts = response.split("Invoice created:")[1].strip().split(" ")
        return parts[0]
    return None


def cleanup_invoice(invoice_number: str):
    """Helper to clean up test invoice"""
    try:
        agent.delete_invoice(invoice_number)
    except:
        pass


# Feature: invoice-agent, Property 1: Invoice retrieval consistency
@given(
    client_name=st.text(min_size=1, max_size=100, alphabet=st.characters(
        whitelist_categories=('Lu', 'Ll', 'Nd'), 
        whitelist_characters=' '
    )),
    total_amount=st.floats(min_value=0.01, max_value=999999.99, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=100, deadline=None)
def test_invoice_retrieval_consistency(client_name, total_amount):
    """
    Property 1: Invoice retrieval consistency
    For any invoice that has been successfully created, querying by its 
    invoice_number should return the same invoice data that was stored.
    
    Validates: Requirements 2.1, 2.2
    """
    # Clean up client_name (remove extra spaces)
    client_name = ' '.join(client_name.split()).strip()
    if not client_name:
        client_name = "TestClient"
    
    # Round total_amount to 2 decimal places
    total_amount = round(total_amount, 2)
    
    # Generate unique invoice number for this test
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
    invoice_number = f"TEST-{timestamp}"
    
    client_email = f"test_{timestamp}@example.com"
    
    try:
        # Create invoice
        create_result = agent.create_invoice(
            client_name=client_name,
            client_email=client_email,
            total_amount=total_amount,
            invoice_number=invoice_number
        )
        
        # Verify creation was successful
        assert "Invoice created:" in create_result or invoice_number in create_result, \
            f"Invoice creation failed: {create_result}"
        
        # Retrieve invoice by number
        retrieve_result = agent.get_invoice_by_number(invoice_number)
        
        # Verify the retrieved data contains the stored data
        assert invoice_number in retrieve_result, \
            f"Invoice number {invoice_number} not found in retrieval result: {retrieve_result}"
        
        assert client_name in retrieve_result, \
            f"Client name '{client_name}' not found in retrieval result: {retrieve_result}"
        
        # Check that total_amount is present (allowing for formatting differences)
        amount_str = f"{total_amount:.2f}"
        assert amount_str in retrieve_result or str(total_amount) in retrieve_result, \
            f"Total amount {total_amount} not found in retrieval result: {retrieve_result}"
        
        # Verify status is 'draft' (default for new invoices)
        assert "draft" in retrieve_result.lower(), \
            f"Status 'draft' not found in retrieval result: {retrieve_result}"
        
    finally:
        # Clean up: delete the test invoice
        cleanup_invoice(invoice_number)


if __name__ == "__main__":
    # Run the property test
    test_invoice_retrieval_consistency()
    print("✅ Property test passed: Invoice retrieval consistency")
