import json
import os
import time
from . import search, scraper, memory

ASSIGNMENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'assignments.json')
DOSSIER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'dossiers')

def process_assignments():
    """
    Reads assignment tickets, performs research, and generates dossiers.
    """
    if not os.path.exists(ASSIGNMENTS_FILE):
        print("Journalist: No assignments file found.")
        return

    with open(ASSIGNMENTS_FILE, 'r') as f:
        tickets = json.load(f)
        
    os.makedirs(DOSSIER_DIR, exist_ok=True)
    
    for ticket in tickets:
        ticket_id = ticket.get('id')
        dossier_path = os.path.join(DOSSIER_DIR, f"{ticket_id}.json")
        
        # Skip if already processed
        if os.path.exists(dossier_path):
            continue
            
        print(f"\nJournalist: Working on Assignment '{ticket['title']}'...")
        
        # 1. Search Tavily
        query = f"{ticket['title']} latest news details"
        search_results = search.search_topic(query)
        
        # 2. Scrape & Store
        facts = []
        for result in search_results[:3]: # Limit to top 3
            url = result['url']
            content = scraper.scrape_url(url)
            if content:
                meta = {"source": url, "title": result.get('title', 'Unknown')}
                memory.store_research(content, meta)
                facts.append(f"Source: {url}\nSummary: {content[:500]}...") # Keep a summary for the dossier
                
        # 3. Compile Dossier
        # In a full agent, we'd loop RAG queries here. 
        # For MVP, we save the search summaries and metadata.
        dossier = {
            "ticket_id": ticket_id,
            "title": ticket['title'],
            "status": "researched",
            "search_results": search_results,
            "key_facts": facts, # Simple list for now
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(dossier_path, 'w') as f:
            json.dump(dossier, f, indent=2)
            
        print(f"Journalist: Dossier saved to {dossier_path}")
        
    print("Journalist: All assignments processed.")
