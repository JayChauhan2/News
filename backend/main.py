
import uvicorn
import threading
import time
import os
import sys

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.api import app
from backend import run_news_cycle

def news_loop():
    """
    Runs the news cycle periodically.
    """
    print("Main: Starting News Loop in background...")
    while True:
        try:
            run_news_cycle.run_cycle()
        except Exception as e:
            print(f"Main: Error in news loop: {e}")
        
        print("Main: Sleeping for 2 minutes...")
        time.sleep(120) # Run every 2 minutes

if __name__ == "__main__":
    # Start the news loop in a separate thread
    news_thread = threading.Thread(target=news_loop, daemon=True)
    news_thread.start()
    
    # Run the API server (blocking)
    print("Main: Starting API Server on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
