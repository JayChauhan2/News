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
    published_links = set()
    
    if os.path.exists(ARTICLES_FILE):
        try:
            with open(ARTICLES_FILE, 'r') as f:
                articles = json.load(f)
                published_titles = {a['headline'] for a in articles if 'headline' in a}
                # Also add title/original_title if present
                published_titles.update({a['title'] for a in articles if 'title' in a})
                published_titles.update({a['original_title'] for a in articles if 'original_title' in a})
                
                published_links = {a['source_link'] for a in articles if 'source_link' in a}
        except json.JSONDecodeError:
            pass
            
    # Deduplicate assignments based on title (simple check + fuzzy match)
    existing_titles = {t['title'] for t in existing_tickets}
    existing_links = {t['source_link'] for t in existing_tickets if 'source_link' in t}
    
    final_tickets = existing_tickets
    
    import difflib
    from backend import llm_client

    def is_similar(title1, title2, threshold=0.85):
        if not title1 or not title2: return False
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

    # Combined sets of everything we know about
    known_titles_set = existing_titles.union(published_titles)
    known_links_set = existing_links.union(published_links)
    
    known_titles_list = list(known_titles_set)
    
    added_count = 0
    for t in new_tickets:
        title = t['title']
        link = t.get('source_link')
        
        # 1. Exact Link Match (Strongest)
        if link and link in known_links_set:
            print(f"Assigner: Skipped duplicate (Link Match): {link}")
            continue
            
        # 2. Exact String Match (Fastest)
        if title in known_titles_set:
            print(f"Assigner: Skipped duplicate (Exact Title): {title}")
            continue
            
        # 3. Fuzzy Match (Fast)
        is_fuzzy_dupe = False
        for known in known_titles_list:
             if is_similar(title, known, threshold=0.80): # Lowered threshold
                 print(f"Assigner: Skipped duplicate (Fuzzy): '{title}' ≈ '{known}'")
                 is_fuzzy_dupe = True
                 break
        if is_fuzzy_dupe: continue
        
        # 4. LLM Semantic Check (The "Judge")
        # Check against the most recent 50 titles (more context)
        recent_context = known_titles_list[:50]
        
        semantic_match = check_semantic_duplicates_batch(title, recent_context)
        
        if semantic_match:
             print(f"Assigner: LLM Judge found duplicate: '{title}' is the same event as '{semantic_match}'")
             continue

        # If it passed all checks, add it
        final_tickets.append(t)
        
        # CRITICAL: Add to our known set so the NEXT ticket in this loop checks against THIS one
        known_titles_set.add(title)
        known_titles_list.insert(0, title) 
        if link: known_links_set.add(link)
        added_count += 1
            
    # Save
    with open(ASSIGNMENTS_FILE, 'w') as f:
        json.dump(final_tickets, f, indent=2)
        
    print(f"Editor: Created {added_count} new assignment tickets. Total pending: {len(final_tickets)}")
    return final_tickets
