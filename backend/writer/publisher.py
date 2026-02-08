import json
import os
import time
from . import agent, reviewer, formatter
from .. import status_manager

DOSSIER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'dossiers')
ARTICLES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'articles.json')

def publish_pending_dossiers():
    """
    Reads processed dossiers and converts them into articles.
    Runs the full Copy Desk chain: Draft -> Review -> Format -> Publish.
    """
    if not os.path.exists(DOSSIER_DIR) or not os.listdir(DOSSIER_DIR):
        print("Writer: No dossiers found.")
        status_manager.update_agent_status("The Senior Reporter", "Journalist", "Idle", "Waiting for new assignments...")
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
        status_manager.update_agent_status("The Senior Reporter", "Journalist", "Drafting", f"Writing article about: {dossier.get('title', 'Unknown Topic')[:30]}...")
        draft = agent.write_article(dossier)
        if not draft:
            continue
            
        # 2. Review (Fact Check)
        status_manager.update_agent_status("The Senior Reporter", "Journalist", "Reviewing", "Fact-checking and reviewing draft...")
        verified_draft = reviewer.review_draft(draft, dossier)
        
        # 3. Format (SEO & Images)
        status_manager.update_agent_status("The Senior Reporter", "Journalist", "Formatting", "Optimizing for SEO and selecting images...")
        final_draft = formatter.format_article(verified_draft)
        
        # 4. Publish
        status_manager.update_agent_status("The Senior Reporter", "Journalist", "Publishing", "Finalizing publication details...")
        final_article = {
            "id": ticket_id,
            "headline": final_draft['headline'],
            "original_title": dossier.get('original_title') or dossier.get('title'), # Original RSS title
            "source_link": dossier.get('source_link'), # Original RSS link
            "category": final_draft.get('category') or dossier.get('category', 'Tech'), # Handle list or string
            "content": final_draft['content'],
            "image_prompt": final_draft['image_prompt'],
            "image_url": dossier.get('images', [None])[0] if dossier.get('images') else None,
            "seo_tags": final_draft.get('seo_tags', []),
            "meta_description": final_draft.get('meta_description', ""),
            "published_at": time.strftime('%Y-%m-%d %H:%M:%S'),
            "author": "The Senior Reporter (AI)"
        }
        
        # Load most recent state of articles to avoid overwrites
        current_articles = []
        if os.path.exists(ARTICLES_FILE):
            try:
                with open(ARTICLES_FILE, 'r') as f:
                    current_articles = json.load(f)
            except json.JSONDecodeError:
                pass
        
        # Double-check if we already have this ID (race condition protection)
        if any(a.get('id') == ticket_id for a in current_articles):
            print(f"Writer: Skipped duplicate '{final_draft['headline']}' (ID: {ticket_id}) - already exists.")
            # Ensure we clean up the duplicate dossier so we don't process it again
            try:
                os.remove(dossier_path)
            except:
                pass
            continue

        current_articles.insert(0, final_article)
        
        try:
            with open(ARTICLES_FILE, 'w') as f:
                json.dump(current_articles, f, indent=2)
            print(f"Writer: Published '{final_article['headline']}' (Tags: {len(final_article['seo_tags'])})")
            
            # Cleanup only after successful save
            os.remove(dossier_path)
            print(f"Writer: Removed processed dossier {filename}")
            
            existing_ids.add(ticket_id) 

            # Remove from Assignments (To stop re-process loop)
            ASSIGNMENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'assignments.json')
            if os.path.exists(ASSIGNMENTS_FILE):
                try:
                    with open(ASSIGNMENTS_FILE, 'r') as af:
                        assignments = json.load(af)
                    
                    # Filter out the published ticket
                    new_assignments = [a for a in assignments if a.get('id') != ticket_id]
                    
                    if len(new_assignments) < len(assignments):
                        with open(ASSIGNMENTS_FILE, 'w') as af:
                            json.dump(new_assignments, af, indent=2)
                        print(f"Writer: Removed ticket {ticket_id} from assignments.")
                except Exception as e:
                    print(f"Writer: Failed to update assignments file: {e}")

        except Exception as e:
            print(f"Writer: Failed to save article or remove dossier {filename}: {e}")

