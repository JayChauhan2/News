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
        source_url = dossier.get('source_link')
        if not source_url and dossier.get('search_results'):
            source_url = dossier['search_results'][0].get('url')
        
        if source_url:
            result['content'] += f"\n\n[Source]({source_url})"
            
        return result
        
    print(f"Writer: Failed to generate article for {dossier.get('ticket_id')}")
    return None
