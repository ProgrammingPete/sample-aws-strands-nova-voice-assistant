#!/usr/bin/env python3

"""
Test Supabase Database Connection

How to run:
    cd /path/to/project
    uv run python test/test_db_connection.py

Expected output:
    "Connection successful! Found X invoices"
    
If connection fails, check:
    - SUPABASE_PASSWORD in .env file
    - Connection string format in the script
    - Network connectivity to Supabase
"""

import os
import psycopg2
from dotenv import load_dotenv

def test_connection():
    # Load environment variables from .env file
    load_dotenv()
    password = os.getenv('SUPABASE_PASSWORD')
    if not password:
        print("SUPABASE_PASSWORD not set")
        return
    
    conn_string = f"postgresql://postgres.emdlwkjdqbsbeeamgffq:{password}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM invoices")
        count = cursor.fetchone()[0]
        print(f"Connection successful! Found {count} invoices")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
