import json
import os
import time
from . import agent, reviewer, formatter

DOSSIER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'dossiers')
ARTICLES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'articles.json')

def publish_pending_dossiers():
    """
    Reads processed dossiers and converts them into articles.
    Runs the full Copy Desk chain: Draft -> Review -> Format -> Publish.
    """
    if not os.path.exists(DOSSIER_DIR):
        print("Writer: No dossiers found.")
        return

    # Load existing articles
    articles = []
    if os.path.exists(ARTICLES_FILE):
        try:
            with open(ARTICLES_FILE, 'r') as f:
                articles = json.load(f)
        except json.JSONDecodeError:
            pass
            
    existing_ids = {a['id'] for a in articles if 'id' in a}
    
    # Process dossiers
    for filename in os.listdir(DOSSIER_DIR):
        if not filename.endswith('.json'):
            continue
            
        dossier_path = os.path.join(DOSSIER_DIR, filename)
        with open(dossier_path, 'r') as f:
            dossier = json.load(f)
            
        ticket_id = dossier.get('ticket_id')
        
        if ticket_id in existing_ids:
            # Cleanup already published dossiers
            try:
                os.remove(dossier_path)
                print(f"Writer: Cleanup - Removed processed dossier {filename}")
            except:
                pass
            continue
            
        # 1. Draft
        draft = agent.write_article(dossier)
        if not draft:
            continue
            
        # 2. Review (Fact Check)
        verified_draft = reviewer.review_draft(draft, dossier)
        
        # 3. Format (SEO & Images)
        final_draft = formatter.format_article(verified_draft)
        
        # 4. Publish
        final_article = {
            "id": ticket_id,
            "headline": final_draft['headline'],
            "content": final_draft['content'],
            "image_prompt": final_draft['image_prompt'],
            "seo_tags": final_draft.get('seo_tags', []),
            "meta_description": final_draft.get('meta_description', ""),
            "published_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            "author": "The Senior Reporter (AI)"
        }
        
        articles.insert(0, final_article) # Add to top
        existing_ids.add(ticket_id) # Update running set
        print(f"Writer: Published '{final_article['headline']}' (Tags: {len(final_article['seo_tags'])})")
        
        # Cleanup
        try:
            os.remove(dossier_path)
            print(f"Writer: Removed processed dossier {filename}")
        except Exception as e:
            print(f"Writer: Failed to remove dossier {filename}: {e}")
            
    # Save all
    with open(ARTICLES_FILE, 'w') as f:
        json.dump(articles, f, indent=2)
