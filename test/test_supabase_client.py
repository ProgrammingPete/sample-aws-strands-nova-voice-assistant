#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from supabase.client import ClientOptions

def test_supabase_connection():
    # Load environment variables
    load_dotenv()
    
    # Initialize supabase connection (same as invoice_agent.py)
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    
    print(f"SUPABASE_URL: {url}")
    print(f"SUPABASE_ANON_KEY: {'*' * 20 if key else 'None'}")
    
    if not url or not key:
        print("ERROR: SUPABASE_URL and SUPABASE_ANON_KEY must be set")
        return
        
    supabase_client: Client = create_client(
        url,
        key,
        options=ClientOptions(
            postgrest_client_timeout=10,
            storage_client_timeout=10,
            schema="api",
        )
    )
    
    print("\n--- Testing Supabase Client ---")
    
    # Test 1: List all invoices
    print("\n1. Testing list all invoices:")
    try:
        response = supabase_client.table("invoices").select("*").execute()
        print(f"Response data: {response.data}")
        print(f"Response count: {response.count}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Get specific invoice
    print("\n2. Testing get invoice INV-001:")
    try:
        response = supabase_client.table("invoices").select("*").eq("invoice_number", "INV-001").execute()
        print(f"Response data: {response.data}")
        print(f"Response count: {response.count}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get invoices by client
    print("\n3. Testing get invoices for John Smith:")
    try:
        response = supabase_client.table("invoices").select("*").eq("client_name", "John Smith").execute()
        print(f"Response data: {response.data}")
        print(f"Response count: {response.count}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_supabase_connection()
