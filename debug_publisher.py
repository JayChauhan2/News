
import os
import json
import sys

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from backend.writer import publisher, agent
try:
    from backend.llm_client import generate_json
except ImportError:
    pass

def debug_dossier(filename):
    dossier_path = os.path.join('public', 'dossiers', filename)
    print(f"DEBUG: Loading {dossier_path}")
    
    with open(dossier_path, 'r') as f:
        dossier = json.load(f)
        
    print("DEBUG: Calling Agent Write Article...")
    draft = agent.write_article(dossier)
    
    if not draft:
        print("DEBUG: Agent returned NONE. Code failed.")
    else:
        print("DEBUG: Agent Success!")
        print(json.dumps(draft, indent=2)[:500])

if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_dossier(sys.argv[1])
