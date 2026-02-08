import json
import os

ARTICLES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'public', 'articles.json')

def fix_duplicates():
    if not os.path.exists(ARTICLES_FILE):
        print("No articles file found.")
        return

    with open(ARTICLES_FILE, 'r') as f:
        articles = json.load(f)

    seen_ids = set()
    cleaned_articles = []
    
    # We want to keep the "best" version of the article.
    # The file is likely ordered new -> old.
    # The duplicates observed had the "bad" version (missing original_title) at the top (newer).
    # And the "good" version (with original_title) below (older).
    # So we should probably scan the list, group by ID, and pick the best one.
    
    from collections import defaultdict
    articles_by_id = defaultdict(list)
    
    for article in articles:
        articles_by_id[article['id']].append(article)
        
    print(f"Total articles: {len(articles)}")
    print(f"Unique IDs: {len(articles_by_id)}")
    
    final_list = []
    
    # Preserve order of FIRST appearance of an ID? Or just reconstruct?
    # Usually we want the newest articles at top.
    # But if the newest is the "bad" duplicate, we want to replace it with the "good" one but keep the position?
    # Or just keep the good one in its original position?
    # Let's simple filter: Iterate through original list. If ID seen, skip?
    # That keeps the TOP (newest) one. Which is the BAD one in our observation.
    
    # Better strategy: Data scrubbing.
    # For each ID, pick the best candidate from the list of duplicates.
    # Then insert that candidate at the position of the *first* occurrence?
    
    # Let's identify the best candidate for each ID.
    best_candidates = {}
    for aid, candidates in articles_by_id.items():
        # Score candidates: +1 if has original_title, +1 if has source_link, +1 if has image_prompt
        best = candidates[0]
        max_score = -1
        
        for c in candidates:
            score = 0
            if c.get('original_title'): score += 1
            if c.get('source_link'): score += 1
            if c.get('image_prompt'): score += 1
            if c.get('category'): score += 1
            
            if score > max_score:
                max_score = score
                best = c
                
        best_candidates[aid] = best

    # Reconstruct list preserving order of first appearance
    seen_ids_final = set()
    for article in articles:
        aid = article['id']
        if aid not in seen_ids_final:
            final_list.append(best_candidates[aid])
            seen_ids_final.add(aid)
            
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(final_list, f, indent=2)
        
    print(f"Cleaned articles saved. Count: {len(final_list)}")

if __name__ == "__main__":
    fix_duplicates()
