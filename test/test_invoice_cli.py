#!/usr/bin/env python3

import sys
import os
import asyncio
sys.path.append('backend/src')

from dotenv import load_dotenv
from voice_based_aws_agent.agents.invoice_agent import InvoiceAgent # pyright: ignore[reportMissingImports]
from voice_based_aws_agent.config.config import AgentConfig # pyright: ignore[reportMissingImports]

def main():
    # Load environment variables
    load_dotenv()
    
    # Load config
    config = AgentConfig()
    
    # Create agent
    agent = InvoiceAgent(config)
    
    print("Invoice Agent CLI Test")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    while True:
        try:
            query = input("\nEnter your query: ").strip()
            
            if query.lower() in ['quit', 'exit', 'q']:
                break
                
            if not query:
                continue
                
            print("\nProcessing...")
            response = agent(query)
            print(f"\nResponse: {response}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("\nGoodbye!")

if __name__ == "__main__":
    main()
