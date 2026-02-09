import json
import os
import time

class MemoryManager:
    def __init__(self, filepath="backend/data/agent_memory.json"):
        # Ensure absolute path
        if not os.path.isabs(filepath):
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.filepath = os.path.join(base_dir, filepath)
        else:
            self.filepath = filepath
            
        self.memory = self._load_memory()
        self.max_items = 1000 # Keep memory size manageable

    def _load_memory(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {"seen_urls": [], "seen_titles": []}
        return {"seen_urls": [], "seen_titles": []}

    def save_memory(self):
        # Enforce limits
        if len(self.memory["seen_urls"]) > self.max_items:
            self.memory["seen_urls"] = self.memory["seen_urls"][-self.max_items:]
        if len(self.memory["seen_titles"]) > self.max_items:
            self.memory["seen_titles"] = self.memory["seen_titles"][-self.max_items:]
            
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            
        with open(self.filepath, 'w') as f:
            json.dump(self.memory, f, indent=2)

    def is_seen(self, url, title):
        # Check URL
        if url in self.memory["seen_urls"]:
            return True
            
        # Check Title (Exact)
        if title in self.memory["seen_titles"]:
            return True
            
        # Check Title (Fuzzy)
        # Check against last 200 titles for performance
        recent_titles = self.memory["seen_titles"][-200:]
        for seen_title in recent_titles:
            if self.is_similar(title, seen_title):
                # print(f"Memory: '{title[:30]}...' is similar to '{seen_title[:30]}...'")
                return True
            
        return False

    def is_similar(self, a, b, threshold=0.85):
        import difflib
        return difflib.SequenceMatcher(None, a, b).ratio() > threshold

    def add(self, url, title):
        if url and url not in self.memory["seen_urls"]:
            self.memory["seen_urls"].append(url)
        
        if title and title not in self.memory["seen_titles"]:
            self.memory["seen_titles"].append(title)
            
        self.save_memory()
