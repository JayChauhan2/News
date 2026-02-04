from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import os

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to data files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARTICLES_FILE = os.path.join(BASE_DIR, 'public', 'articles.json')
ASSIGNMENTS_FILE = os.path.join(BASE_DIR, 'public', 'assignments.json')

def load_json(filepath):
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

from fastapi.responses import JSONResponse

@app.get("/")
def read_root():
    return {"status": "The Printing Press is running"}

@app.get("/articles")
def get_articles():
    content = load_json(ARTICLES_FILE)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate", 
        "Pragma": "no-cache", 
        "Expires": "0"
    }
    return JSONResponse(content=content, headers=headers)

@app.get("/assignments")
def get_assignments():
    content = load_json(ASSIGNMENTS_FILE)
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate", 
        "Pragma": "no-cache", 
        "Expires": "0"
    }
    return JSONResponse(content=content, headers=headers)

import threading
import time
from backend.writer import publisher

def run_publisher_loop():
    while True:
        try:
            publisher.publish_pending_dossiers()
        except Exception as e:
            print(f"Publisher Loop Error: {e}")
        time.sleep(10)

@app.on_event("startup")
def startup_event():
    # Start publisher in background thread
    t = threading.Thread(target=run_publisher_loop, daemon=True)
    t.start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
