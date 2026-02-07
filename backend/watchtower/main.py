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
from backend.watchtower import trend_spotter

CATEGORIES_LIST = [
    "World", "Business", "U.S.", "Politics", "Economy", "Tech", "Markets & Finance", 
    "Opinion", "Free Expression", "Arts", "Lifestyle", "Real Estate", 
    "Personal Finance", "Health", "Style", "Sports"
]

def job():
    print(f"\n[{time.strftime('%H:%M:%S')}] Watchtower Cycle Started")
    
    for category in CATEGORIES_LIST:
        print(f"\n--- Processing Category: {category} ---")
        
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
            clusters = clustering.deduplicate_news(articles)
            
            # 3. Score & Assign
            scored_clusters = []
            print(f"[{time.strftime('%H:%M:%S')}] Editor: Scoring {len(clusters)} clusters for {category}...")
            
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
