#!/usr/bin/env python3

import sys
import os
import asyncio
sys.path.append('backend/src')

from dotenv import load_dotenv
from voice_based_aws_agent.agents.invoice_agent import InvoiceAgent # pyright: ignore[reportMissingImports]
from voice_based_aws_agent.config.config import AgentConfig # pyright: ignore[reportMissingImports]

async def test_invoice_agent_batch():
    # Load environment variables
    load_dotenv()
    
    # Load config
    config = AgentConfig()
    
    # Create agent
    agent = InvoiceAgent(config)
    
    # Test queries
    test_queries = [
        "List all invoices",
        "Show me invoices for John Smith",
        "What's the status of invoice INV-001?",
        "Get invoice details for INV-001",
        "Show me all unpaid invoices",
        "Create a new invoice where the user is Peter Parianos and the amount is 10000, with email peter.parianos@canvalo.com and Invoice number INV-003 and due date december 5 2024",
        "Delete invoice INV-003"
    ]
    
    print("=== Invoice Agent Batch Test ===\n")
    
    for i, query in enumerate(test_queries, 1):
        print(f"Test {i}: {query}")
        print("-" * 50)
        try:
            response = await agent.invoke_async(query)
            print(f"Response: {response}\n")
        except Exception as e:
            print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_invoice_agent_batch())
