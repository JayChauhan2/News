import json
import os

# A simple JSON file to act as memory for now
MEMORY_FILE = "journalist_memory.json"

def store_research(text, metadata):
    """
    Stores text chunks in a simple JSON file.
    """
    if not text:
        return
        
    print(f"Journalist: Storing {len(text)} chars to simple memory...")
    
    entries = []
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                entries = json.load(f)
        except:
            pass
            
    # Just store the whole chunk with metadata
    entries.append({"text": text, "metadata": metadata})
    
    with open(MEMORY_FILE, 'w') as f:
        json.dump(entries, f)

def query_research(question, n_results=3):
    """
    Retrieves relevant context (Naive match).
    """
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, 'r') as f:
            entries = json.load(f)
            
        # Naive keyword matching
        keywords = question.lower().split()
        results = []
        for entry in entries:
            score = 0
            for kw in keywords:
                if kw in entry['text'].lower():
                    score += 1
            if score > 0:
                results.append((score, entry['text']))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:n_results]]
        
    except Exception as e:
        print(f"Error querying memory: {e}")
        return []
