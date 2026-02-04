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

def job():
    print(f"\n[{time.strftime('%H:%M:%S')}] Watchtower Job Started")
    # 1. Fetch
    articles = sources.fetch_all_news()
    
    # 2. Filter / Deduplicate (Clustering)
    if articles:
        clusters = clustering.deduplicate_news(articles)
        
        # 3. Score & Assign
        scored_clusters = []
        print(f"[{time.strftime('%H:%M:%S')}] Editor: Scoring {len(clusters)} clusters (Throttled to Top 3)...")
        # Throttle: Only process top 3 clusters to prevent rate limit spikes
        for cluster in clusters[:3]:
            # Score the first article as representative
            score_data = scoring.score_article(cluster[0])
            scored_clusters.append((cluster, score_data))
            
        # 4. Create Assignments
        assigner.create_assignments(scored_clusters)
        
        # 5. Run Journalist (Research)
        print(f"[{time.strftime('%H:%M:%S')}] Journalist: Starting research on pending tickets...")
        dossier.process_assignments()
        
        # 6. Run Writer (Publish)
        print(f"[{time.strftime('%H:%M:%S')}] Writer: Publishing pending dossiers...")
        publisher.publish_pending_dossiers()
        
        # 7. Save Raw Data (Optional, but good for debugging)
        storage.save_news(articles)
        print(f"[{time.strftime('%H:%M:%S')}] Job Completed.")
    else:
        print("No articles found.")

def main():
    print("Starting The Watchtower Agent...")
    print("Press Ctrl+C to stop.")
    
    # Run once immediately on startup
    job()
    
    # Schedule to run every 10 minutes
    schedule.every(10).minutes.do(job)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
