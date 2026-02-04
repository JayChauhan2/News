from . import prompts
from llm_client import generate_json
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
    
    user_prompt = f"""
    Here is the Research Dossier. Use these facts to write the article.
    Do NOT make up facts not present here.
    
    Title: {dossier['title']}
    
    Key Facts:
    {facts_text}
    
    Search Context:
    {search_summary}
    
    Output ONLY a JSON object with the following structure:
    {{
        "headline": "A catchy, click-worthy headline",
        "content": "The full markdown article content...",
        "image_prompt": "A description for an AI image generator to create a hero image"
    }}
    """
    
    result = generate_json(system_prompt + "\nYou helpfully output valid JSON.", user_prompt, temperature=0.7)
    
    if result:
         # Generate image prompt if missing
        if 'image_prompt' not in result:
             result['image_prompt'] = f"A photo representing {result.get('headline', 'news')}"
        return result
        
    print(f"Writer: Failed to generate article for {dossier.get('ticket_id')}")
    return None
