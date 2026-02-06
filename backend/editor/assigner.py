import json
import os
import time

ASSIGNMENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'assignments.json')
ARTICLES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'articles.json')

def create_assignments(scored_clusters):
    """
    Takes a list of (cluster, score_data) tuples.
    Creates tickets for high-scoring items (> 7).
    Saves to public/assignments.json.
    """
    new_tickets = []
    
    for cluster, score_data in scored_clusters:
        if score_data['score'] >= 5:
            # Create a ticket from the most representative article (the first one)
            main_article = cluster[0]
            
            ticket = {
                "id": str(int(time.time())) + "_" + str(len(new_tickets)), # Simple ID
                "status": "pending",
                "score": score_data['score'],
                "reasoning": score_data['reasoning'],
                "title": main_article['title'],
                "source_link": main_article['link'],
                "cluster_size": len(cluster),
                "created_at": time.strftime('%Y-%m-%d %H:%M:%S')
            }
            new_tickets.append(ticket)
            
    # Load existing tickets to append
    existing_tickets = []
    if os.path.exists(ASSIGNMENTS_FILE):
        try:
            with open(ASSIGNMENTS_FILE, 'r') as f:
                existing_tickets = json.load(f)
        except json.JSONDecodeError:
            pass

    # Load published articles to check for duplicates
    published_titles = set()
    if os.path.exists(ARTICLES_FILE):
        try:
            with open(ARTICLES_FILE, 'r') as f:
                articles = json.load(f)
                published_titles = {a['headline'] for a in articles if 'headline' in a}
                # Also add title if present (old format)
                published_titles.update({a['title'] for a in articles if 'title' in a})
        except json.JSONDecodeError:
            pass
            
    # Deduplicate assignments based on title (simple check)
    existing_titles = {t['title'] for t in existing_tickets}
    final_tickets = existing_tickets
    
    added_count = 0
    for t in new_tickets:
        if t['title'] not in existing_titles and t['title'] not in published_titles:
            final_tickets.append(t)
            added_count += 1
            
    # Save
    with open(ASSIGNMENTS_FILE, 'w') as f:
        json.dump(final_tickets, f, indent=2)
        
    print(f"Editor: Created {added_count} new assignment tickets. Total pending: {len(final_tickets)}")
    return final_tickets
