
import asyncio
import sys
import os
import sqlite3
import json

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower.x_scraper import add_account, pool, DB_FILE

async def main():
    print("--- Add X/Twitter Account via Cookies (Bypass Cloudflare) ---")
    print("This script adds an account and injects cookies directly to bypass the login screen.")
    print("You will need 'ct0' and 'auth_token' cookies from your browser.")
    print("1. Log in to X.com in your browser.")
    print("2. Open Developer Tools (F12) -> Application -> Cookies.")
    print("3. Find 'ct0' and 'auth_token' and copy their values.")
    
    username = input("\nUsername (without @): ").strip()
    if not username:
        return

    password = input("Password (used for reference): ").strip()
    email = input("Email (used for reference): ").strip()
    email_password = input("Email Password (used for reference): ").strip()
    
    ct0 = input("Cookie 'ct0': ").strip()
    auth_token = input("Cookie 'auth_token': ").strip()
    
    if not ct0 or not auth_token:
        print("Error: content of cookies cannot be empty.")
        return

    # 1. Add account to DB (standard way)
    print(f"Adding account {username} to database...")
    try:
        await add_account(username, password, email, email_password)
    except Exception as e:
        print(f"Note: {e}") 
        # proceed even if it says account exists, we will update it
    
    # 2. Manually update cookies and set active=1
    print("Injecting cookies...")
    
    cookies_dict = {
        "ct0": ct0,
        "auth_token": auth_token
    }
    cookies_json = json.dumps(cookies_dict)
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Update cookies and set active=1 (true)
        # We also clear any error_msg
        cursor.execute("""
            UPDATE accounts 
            SET cookies = ?, active = 1, error_msg = NULL
            WHERE username = ? COLLATE NOCASE
        """, (cookies_json, username))
        
        if cursor.rowcount == 0:
            print("Error: Account not found in DB even after adding.")
        else:
            print("Cookies injected successfully. Account marked as ACTIVE.")
            
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Database error: {e}")
        return

    print("\nVerification skipped (to avoid triggering Cloudflare again immediately).")
    print("You can now run the monitor.")

if __name__ == "__main__":
    asyncio.run(main())
