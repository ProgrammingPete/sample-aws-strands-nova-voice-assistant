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
    conn_string = os.getenv('SUPABASE_POOL_CONNECTION')
    if not conn_string:
        print("SUPABASE_CONNECTION not set")
        return
    
    try:
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM invoices")
        result = cursor.fetchone()
        if result:
            count = result[0]
            print(f"Connection successful! Found {count} invoices")
        else:
            print("Connection successful but no data returned")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connection()
