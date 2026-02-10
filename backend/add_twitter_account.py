
import asyncio
import sys
import os

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower.x_scraper import add_account, pool

async def main():
    print("--- Add X/Twitter Account for Scraper ---")
    print("This script adds an account to the local 'accounts.db' for twscrape.")
    print("You will need the username, password, email, and email password.")
    
    while True:
        username = input("Username (without @): ").strip()
        if not username:
             break
             
        password = input("Password: ").strip()
        email = input("Email: ").strip()
        email_password = input("Email Password: ").strip()
        
        print(f"Adding account {username}...")
        await add_account(username, password, email, email_password)
        
        cont = input("Add another account? (y/n): ").lower()
        if cont != 'y':
            break

    print("\nDone. Verifying accounts...")
    try:
        await pool.login_all()
        print("Accounts verified.")
    except Exception as e:
        print(f"Error verifying accounts: {e}")

if __name__ == "__main__":
    asyncio.run(main())
