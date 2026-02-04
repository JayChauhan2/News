from backend.llm_client import generate_json

def format_article(draft):
    """
    Optimizes the article for publication (SEO, Meta, Image Prompt refinement).
    """
    prompt = f"""
    You are the SEO Editor.
    Optimize the metadata for this article.
    
    Headline: {draft.get('headline')}
    Content: {draft.get('content')[:1000]}... (truncated)
    Current Image Prompt: {draft.get('image_prompt')}
    
    Tasks:
    1. Generate 5 relevant SEO hashtags.
    2. Write a compelling meta description (max 160 chars).
    3. Refine the image prompt to be specifically optimized for DALL-E 3 (photorealistic, dramatic lighting, 16:9).
    
    Output ONLY a JSON object:
    {{
        "seo_tags": ["#tag1", "#tag2", ...],
        "meta_description": "...",
        "hero_image_prompt": "Refined DALL-E 3 prompt..."
    }}
    """
    
    print(f"Copy Desk: Formatting '{draft['headline']}'...")
    
    formatting_data = generate_json("You are a helpful assistant that outputs JSON only.", prompt, temperature=0.5)
    
    if formatting_data:
        # Merge results
        final_article = draft.copy()
        final_article['seo_tags'] = formatting_data.get('seo_tags', [])
        final_article['meta_description'] = formatting_data.get('meta_description', "")
        final_article['image_prompt'] = formatting_data.get('hero_image_prompt', draft.get('image_prompt'))
        
        return final_article
        
    return draft
