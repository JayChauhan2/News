import schedule
import time
import sources
import storage
import sys
import os

# Add the project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.editor import clustering, scoring, assigner
from backend.journalist import dossier
from backend.writer import publisher
from backend.writer import publisher
from backend.watchtower import trend_spotter
from backend import status_manager

CATEGORIES_LIST = [
    "World", "Politics", "Business", "Tech", "Startups", "Science", "Opinion"
]


def job():
    print(f"\n[{time.strftime('%H:%M:%S')}] Watchtower Cycle Started")
    status_manager.update_agent_status("The Watchtower", "News Monitor", "Active", "Starting new scan cycle...")
    
    for category in CATEGORIES_LIST:
        print(f"\n--- Processing Category: {category} ---")
        status_manager.update_agent_status("The Watchtower", "News Monitor", "Scanning", f"Scanning for {category} news...")
        
        # 1. Fetch
        rss_articles = sources.fetch_rss_news(category)
        try:
            web_articles = trend_spotter.fetch_trending_news(category)
        except Exception as e:
            print(f"Trend Spotter failed for {category}: {e}")
            web_articles = []
        
        articles = rss_articles + web_articles
        
        # 2. Filter / Deduplicate (Clustering)
        if articles:
            status_manager.update_agent_status("The Watchtower", "News Monitor", "Filtering", f"Filtering {len(articles)} articles in {category}...")
            clusters = clustering.deduplicate_news(articles)
            
            # 3. Score & Assign
            scored_clusters = []
            print(f"[{time.strftime('%H:%M:%S')}] Editor: Scoring {len(clusters)} clusters for {category}...")
            # Status update for Editor is handled in filtering/scoring modules or here? 
            # Better to let the Editor modules handle their own status if they are called as libraries.
            # But the 'Editor' isn't a running process, it's a library called by Watchtower. 
            # So Watchtower is effectively the runner for the Editor.
            # However, to simulate 'The Chief Editor' agent, we should update ITS status here or inside the functions.
            # I will update it here for high level 'Scoring' status, and inside for granular 'Scoring X'.
            
            # Throttle: Only process Top 1 cluster per category to keep volume manageable (16 categories * 1 = 16 potential stories)
            for cluster in clusters[:1]:
                # Score the first article as representative
                try:
                    score_data = scoring.score_article(cluster[0])
                    scored_clusters.append((cluster, score_data))
                except Exception as e:
                    print(f"Scoring failed: {e}")
                
            # 4. Create Assignments
            assigner.create_assignments(scored_clusters)
            
            # 5. Run Journalist (Research)
            print(f"[{time.strftime('%H:%M:%S')}] Journalist: Researching...")
            dossier.process_assignments()
            
            # 6. Run Writer (Publish)
            print(f"[{time.strftime('%H:%M:%S')}] Writer: Publishing...")
            publisher.publish_pending_dossiers()
            
            # 7. Save Raw Data
            storage.save_news(articles)
        else:
            print(f"No articles found for {category}.")
            
    print(f"[{time.strftime('%H:%M:%S')}] Cycle Completed.")
    status_manager.update_agent_status("The Watchtower", "News Monitor", "Idle", "Waiting for next cycle...")

def main():
    print("Starting The Watchtower Agent (Continuous Mode)...")
    print("Press Ctrl+C to stop.")
    
    while True:
        try:
            job()
            print(f"[{time.strftime('%H:%M:%S')}] Cycle complete. Sleeping for 60 seconds...")
        except Exception as e:
             print(f"Error in Watchtower loop: {e}")
        
        time.sleep(60)

if __name__ == "__main__":
    main()
