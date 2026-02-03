import schedule
import time
import sources
import storage

def job():
    print(f"\n[{time.strftime('%H:%M:%S')}] Watchtower Job Started")
    # 1. Fetch
    articles = sources.fetch_all_news()
    
    # 2. Filter / Deduplicate (Placeholder for now)
    # unique_articles = filter_data(articles)
    
    # 3. Save
    if articles:
        storage.save_news(articles)
        print(f"[{time.strftime('%H:%M:%S')}] Job Completed. {len(articles)} articles currently available.")
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
