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
                "category": main_article.get("category", "Tech"),
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
            
    # Deduplicate assignments based on title (simple check + fuzzy match)
    existing_titles = {t['title'] for t in existing_tickets}
    final_tickets = existing_tickets
    
    import difflib
    from backend import llm_client

    def is_similar(title1, title2, threshold=0.85):
        return difflib.SequenceMatcher(None, title1.lower(), title2.lower()).ratio() > threshold

    def check_semantic_duplicates_batch(new_title, existing_titles_list):
        if not existing_titles_list:
             return None
             
        # Only check against last 30 to save tokens/time
        recent_titles = list(existing_titles_list)[:30]
        
        prompt = f"""
        You are a smart News Editor. 
        Determine if the NEW HEADLINE is reporting on the SAME SPECIFIC EVENT as any of the EXISTING HEADLINES.
        
        NEW HEADLINE: "{new_title}"
        
        EXISTING HEADLINES:
        {json.dumps(recent_titles, indent=2)}
        
        Rules:
        - "Same event" means they cover the same core duplicate story (e.g. "Earthquake in Japan" vs "7.0 Magnitude Quake hits Tokyo").
        - If matches, return the EXACT/IDENTICAL duplicate headline from the list.
        - If no match, return "None".
        - Output only the string of the matching headline or "None".
        """
        try:
            result = llm_client.generate_json("You output a JSON with key 'match' which is the string or null.", prompt)
            # Fallback if it returns raw text
            if not isinstance(result, dict): 
                 match = str(result).strip()
                 return match if match in recent_titles else None
            return result.get("match")
        except:
            return None

    added_count = 0
    for t in new_tickets:
        if t['title'] in existing_titles or t['title'] in published_titles:
            continue
            
        # Fuzzy check against assignments
        is_duplicate = False
        for ex_ticket in existing_tickets:
             if is_similar(t['title'], ex_ticket['title']):
                 print(f"Assigner: Skipped duplicate (similar to pending): '{t['title']}' ≈ '{ex_ticket['title']}'")
                 is_duplicate = True
                 break
        if is_duplicate: continue

        # Fuzzy check against published articles
        for title in published_titles:
             if is_similar(t['title'], title):
                 print(f"Assigner: Skipped duplicate (similar to published): '{t['title']}' ≈ '{title}'")
                 is_duplicate = True
                 break
        if is_duplicate: continue

        # --- LLM Semantic Check (The "Judge") ---
        # Combine distinct titles to check against
        all_existing = list(existing_titles.union(published_titles))
        semantic_match = check_semantic_duplicates_batch(t['title'], all_existing)
        
        if semantic_match:
             print(f"Assigner: LLM Judge found duplicate: '{t['title']}' is the same event as '{semantic_match}'")
             continue

        final_tickets.append(t)
        added_count += 1
            
    # Save
    with open(ASSIGNMENTS_FILE, 'w') as f:
        json.dump(final_tickets, f, indent=2)
        
    print(f"Editor: Created {added_count} new assignment tickets. Total pending: {len(final_tickets)}")
    return final_tickets
