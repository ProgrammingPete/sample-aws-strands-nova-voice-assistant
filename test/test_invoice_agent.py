#!/usr/bin/env python3

import sys
import os
import asyncio
sys.path.append('backend/src')

from dotenv import load_dotenv
from voice_based_aws_agent.agents.invoice_agent import InvoiceAgent
from voice_based_aws_agent.config.config import AgentConfig

async def test_invoice_agent():
    # Load environment variables
    load_dotenv()
    
    # Load config
    config = AgentConfig()
    
    # Create agent
    agent = InvoiceAgent(config)
    
    # Test queries
    test_queries = [
        "List all invoices",
        "Show me invoices for Acme Corp",
        "What's the status of invoice INV-001?"
    ]
    
    for query in test_queries:
        print(f"\n--- Testing: {query} ---")
        try:
            response = await agent.invoke_async(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_invoice_agent())
