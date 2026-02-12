
import asyncio
import sys
import os
import sqlite3

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower.x_scraper import pool, DB_FILE

async def main():
    print("--- Fix Scraper Blocking ---")
    print("This script will:")
    print("1. Reset the 'timeout' locks on your accounts.")
    print("2. (Optional) Update the User-Agent to match your browser exactly.")
    
    print("\nResetting locks...")
    await pool.reset_locks()
    print("Locks reset.")
    
    print("\n--- User Agent Update ---")
    print("To bypass Cloudflare, your scraper should pretend to be your exact browser.")
    print("Check your browser's User-Agent (search 'my user agent' on Google).")
    print("Example: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...")
    
    ua = input("Paste your User-Agent here (or press Enter to skip): ").strip()
    
    if ua:
        try:
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            
            # Update all accounts to use this UA
            cursor.execute("UPDATE accounts SET user_agent = ?", (ua,))
            
            if cursor.rowcount > 0:
                print(f"Updated User-Agent for {cursor.rowcount} accounts.")
            else:
                print("No accounts found to update.")
                
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error updating DB: {e}")
    
    print("\nDone. Try running the monitor again.")

if __name__ == "__main__":
    asyncio.run(main())
