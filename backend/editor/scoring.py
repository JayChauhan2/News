from backend.llm_client import generate_json
from backend import status_manager

def score_article(article):
    """
    Uses LLM to score the article based on headline and summary.
    """
    title = article.get('title', 'Unknown')
    status_manager.update_agent_status("The Chief Editor", "Editor-in-Chief", "Scoring", f"Evaluating editorial value of: {title[:40]}...")
    
    import datetime
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    prompt = f"""
    You are the Editor-in-Chief.
    Today's date is {today}.
    Analyze this news story:
    Headline: {article.get('title')}
    Summary: {article.get('summary')}
    
    Score it on:
    1. Impact (0-10): How big is this news?
    2. Novelty (0-10): Is it new info?
    3. Relevance (0-10): Is it tech/AI related?
    
    Output ONLY a JSON object:
    {{
        "impact": 8,
        "novelty": 7,
        "relevance": 9,
        "reasoning": "Short explanation..."
    }}
    """
    
    result = generate_json("You are a helpful assistant that outputs JSON only.", prompt)
    
    if result:
         # Calculate total score from whatever fields are present, adapting if model output varies
        score = result.get('score', 0)
        # Or if it output individual fields
        if 'impact' in result:
             score = (result.get('impact', 0) + result.get('novelty', 0) + result.get('relevance', 0)) / 3
             
        return {
            "score": round(score, 1),
            "reasoning": result.get('reasoning', "No reasoning provided.")
        }
    
    return {"score": 0, "reasoning": "Error during scoring."}
