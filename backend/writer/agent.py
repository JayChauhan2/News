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
    
    # Construct the user prompt with facts
    facts_text = "\n".join(dossier.get('key_facts', []))
    search_summary = json.dumps(dossier.get('search_results', []), indent=2)
    
    current_date = datetime.datetime.now().strftime('%A, %B %d, %Y')
    
    user_prompt = f"""
    Here is the Research Dossier. Use these facts to write the article.
    Current Date: {current_date}
    Do NOT make up facts not present here.
    
    Title: {dossier['title']}
    Target Category: {dossier.get('category', 'Tech')} (You may add a second relevant category if needed)
    Available Categories: World, Business, U.S., Politics, Economy, Tech, Markets & Finance, Opinion, Free Expression, Arts, Lifestyle, Real Estate, Personal Finance, Health, Style, Sports.
    
    Key Facts:
    {facts_text}
    
    Search Context:
    {search_summary}
    
    Output ONLY a JSON object with the following structure:
    {{
        "headline": "A catchy, click-worthy headline",
        "category": ["Category1", "OptionalCategory2"], 
        "content": "The full markdown article content...",
        "image_prompt": "A description for an AI image generator to create a hero image"
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
