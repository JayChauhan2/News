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
        images = []
        for result in search_results[:3]: # Limit to top 3
            url = result['url']
            scrape_data = scraper.scrape_url(url)
            
            if isinstance(scrape_data, dict) and scrape_data.get('text'):
                content = scrape_data['text']
                image = scrape_data.get('image')
                
                if image:
                    images.append(image)
                
                meta = {"source": url, "title": result.get('title', 'Unknown')}
                memory.store_research(content, meta)
                facts.append(f"Source: {url}\nSummary: {content[:500]}...") # Keep a summary
                 # Fallback for legacy
                 meta = {"source": url, "title": result.get('title', 'Unknown')}
                 memory.store_research(scrape_data, meta)
                 facts.append(f"Source: {url}\nSummary: {scrape_data[:500]}...")
                 
        # 3. Fallback Image Search
        if not images:
            print("Journalist: No images found in articles. Searching online...")
            try:
                found_images = search.search_images(ticket['title'])
                if found_images:
                    images.extend(found_images)
                    print(f"Journalist: Found {len(found_images)} images online.")
            except Exception as e:
                print(f"Journalist: Image search failed: {e}")
                
        # 4. Compile Dossier
        # In a full agent, we'd loop RAG queries here. 
        # For MVP, we save the search summaries and metadata.
        dossier = {
            "ticket_id": ticket_id,
            "ticket_id": ticket_id,
            "title": ticket['title'],
            "original_title": ticket['title'], # Explicitly save for dedup
            "source_link": ticket.get('source_link'), # Save for dedup
            "category": ticket.get("category", "Tech"),
            "status": "researched",
            "search_results": search_results,
            "images": images,
            "key_facts": facts, # Simple list for now
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(dossier_path, 'w') as f:
            json.dump(dossier, f, indent=2)
            
        print(f"Journalist: Dossier saved to {dossier_path}")
        
    print("Journalist: All assignments processed.")
