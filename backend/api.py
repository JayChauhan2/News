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

@app.get("/")
def read_root():
    return {"status": "The Printing Press is running"}

@app.get("/articles")
def get_articles():
    return load_json(ARTICLES_FILE)

@app.get("/assignments")
def get_assignments():
    return load_json(ASSIGNMENTS_FILE)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
