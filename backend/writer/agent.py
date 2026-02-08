from . import prompts
from backend.llm_client import generate_json
import datetime
import json

def write_article(dossier, style="WITTY"):
    """
    Uses LLM to write a full article based on the dossier.
    """
    print(f"Writer: Writing article for ticket {dossier.get('ticket_id')}...")
    
    system_prompt = prompts.WITTY_TECH_BLOGGER if style == "WITTY" else prompts.SERIOUS_ANALYST
    
    # Construct the user prompt with rich data
    angle = dossier.get("angle", "General Overview")
    rationale = dossier.get("angle_rationale", "")
    
    quotes_text = "\n".join([f"- {q['source']}: \"{q['quote']}\"" for q in dossier.get("key_quotes", [])])
    if not quotes_text:
        quotes_text = "No direct quotes available."
        
    facts_text = "\n".join(dossier.get('key_facts', []))
    missing_context = dossier.get("missing_context", "None identified.")
    
    current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
    
    user_prompt = f"""
    The Research Dossier is ready. Write the article now.
    Current Date: {current_date}
    
    --------------------------------------------------
    THE ASSIGNMENT
    Lead Title: {dossier['title']}
    Target Category: {dossier.get('category', 'Tech')}
    
    YOUR ANGLE: {angle}
    Rationale: {rationale}
    --------------------------------------------------
    
    PRIMARY SOURCES & QUOTES (Use these!):
    {quotes_text}
    
    KEY FACTS & CONTEXT:
    {facts_text}
    
    NEGATIVE SPACE (What is missing/hidden):
    {missing_context}
    
    --------------------------------------------------
    Output ONLY a JSON object with the following structure:
    {{
        "headline": "A sharp, angle-driven headline",
        "category": ["Category1", "OptionalCategory2"], 
        "content": "The full markdown article content...",
        "image_prompt": "A description for an AI image generator to create a hero image matching the angle"
    }}
    """
    
    result = generate_json(system_prompt + "\nYou helpfully output valid JSON.", user_prompt, temperature=0.7)
    
    if result:
         # Generate image prompt if missing
        if 'image_prompt' not in result:
             result['image_prompt'] = f"A photo representing {result.get('headline', 'news')}"

        # Append source link
        # Append source link
        source_url = dossier.get('source_link')
        
        # If no direct source link (or if it's just a generic twitter home link), try to find a better primary source from search results
        if (not source_url or "twitter.com" in source_url) and dossier.get('search_results'):
            # Try to find a non-news, primary source (e.g. .gov, .edu, or official company blog)
            best_source = None
            for res in dossier['search_results']:
                url = res.get('url', '')
                # Prioritize official domains
                if '.gov' in url or '.edu' in url or 'blog' in url or 'press' in url:
                    best_source = url
                    break
                
                # Avoid known news aggregators if possible
                if not any(x in url for x in ['nytimes', 'cnn', 'bbc', 'reuters', 'bloomberg', 'cnbc', 'theverge']):
                     if not best_source:
                         best_source = url
            
            if best_source:
                source_url = best_source
            elif not source_url and dossier['search_results']:
                 source_url = dossier['search_results'][0].get('url')
        
        if source_url:
            result['content'] += f"\n\n[Primary Source]({source_url})"
            
        return result
        
    print(f"Writer: Failed to generate article for {dossier.get('ticket_id')}")
    return None
