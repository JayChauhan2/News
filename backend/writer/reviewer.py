from llm_client import generate_json

def review_draft(draft, dossier):
    """
    Checks the draft article against the dossier facts.
    Returns the corrected (or approved) draft.
    """
    facts_text = "\n".join(dossier.get('key_facts', []))
    
    prompt = f"""
    You are the Fact Checker for a news outlet.
    Your job is to compare the Draft Article against the Verified Facts.
    
    Verified Facts:
    {facts_text}
    
    Draft Article:
    Headline: {draft.get('headline')}
    Content: {draft.get('content')}
    
    Instructions:
    1. Identify any claims in the Draft that strictly CONTRADICT the Verified Facts.
    2. Rewrite the content to correct these errors.
    3. If the Draft is fine, return it as is.
    4. Fix any glaring typos.
    
    Output ONLY a JSON object:
    {{
        "headline": "The (possibly corrected) headline",
        "content": "The (possibly corrected) markdown content",
        "image_prompt": "{draft.get('image_prompt')}"
    }}
    """
    
    print(f"Copy Desk: Fact-checking '{draft['headline']}'...")
    
    result = generate_json("You are a helpful assistant that outputs JSON only.", prompt, temperature=0.1)
    
    if result:
        result['ticket_id'] = draft.get('ticket_id')
        return result
        
    return draft
