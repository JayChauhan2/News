
import os
import sys
import json
import time

# Ensure backend path is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.watchtower import trend_spotter
from backend.journalist import dossier
from backend.writer import publisher
from backend import maintainer

ASSIGNMENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'public', 'assignments.json')

def save_assignments(leads):
    """
    Saves new leads to assignments.json, avoiding duplicates.
    """
    if not leads:
        return

    current_assignments = []
    if os.path.exists(ASSIGNMENTS_FILE):
        try:
            with open(ASSIGNMENTS_FILE, 'r') as f:
                current_assignments = json.load(f)
        except json.JSONDecodeError:
            pass
    
    # Simple Deduplication by title/link
    existing_links = {a.get('source_link') for a in current_assignments}
    existing_titles = {a.get('title') for a in current_assignments}
    
    new_count = 0
    for lead in leads:
        if lead.get('link') in existing_links:
            continue
        if lead.get('title') in existing_titles:
            continue
            
        new_assignment = {
            "id": f"ticket_{int(time.time())}_{new_count}", # Simple ID generation
            "title": lead.get('title'),
            "source_link": lead.get('link'),
            "category": lead.get('category', 'Tech'),
            "status": "pending",
            "created_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        current_assignments.append(new_assignment)
        existing_links.add(lead.get('link'))
        new_count += 1
        
    if new_count > 0:
        with open(ASSIGNMENTS_FILE, 'w') as f:
            json.dump(current_assignments, f, indent=2)
        print(f"Cycle: Created {new_count} new assignments.")
    else:
        print("Cycle: No new unique assignments created.")

def run_cycle():
    print(f"\n[{time.strftime('%H:%M:%S')}] --- STARTING NEWS CYCLE ---")
    
    # 1. Watchtower (Trend Spotting)
    # We scan for multiple categories
    categories = ["Tech", "Business", "Science", "World"]
    all_leads = []
    
    for cat in categories:
        try:
            leads = trend_spotter.fetch_social_news(category=cat)
            all_leads.extend(leads)
        except Exception as e:
            print(f"Cycle: Error fetching {cat}: {e}")
            
    # 2. Assign (Save to JSON)
    save_assignments(all_leads)
    
    # 3. Journalist (Research)
    try:
        dossier.process_assignments()
    except Exception as e:
        print(f"Cycle: Error in Journalist phase: {e}")
        
    # 4. Writer (Publish)
    try:
        publisher.publish_pending_dossiers()
    except Exception as e:
        print(f"Cycle: Error in Writer phase: {e}")
        
    # 5. Maintainer (Cleanup)
    try:
        maintainer.run_maintainer()
    except Exception as e:
        print(f"Cycle: Error in Maintainer phase: {e}")
        
    print(f"[{time.strftime('%H:%M:%S')}] --- CYCLE COMPLETE ---")

if __name__ == "__main__":
    run_cycle()
