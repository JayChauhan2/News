import json
import os
import time
from . import search, scraper, memory, prompts
from backend import status_manager, llm_client

ASSIGNMENTS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'assignments.json')
DOSSIER_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'public', 'dossiers')

def process_assignments():
    """
    Reads assignment tickets, performs deep investigation, and generates enhanced dossiers.
    """
    if not os.path.exists(ASSIGNMENTS_FILE):
        print("Journalist: No assignments file found.")
        return

    with open(ASSIGNMENTS_FILE, 'r') as f:
        tickets = json.load(f)
        
    os.makedirs(DOSSIER_DIR, exist_ok=True)
    
    if not tickets:
        status_manager.update_agent_status("The Investigative Journalist", "Journalist", "Idle", "Waiting for leads...")
    
    for ticket in tickets:
        ticket_id = ticket.get('id')
        dossier_path = os.path.join(DOSSIER_DIR, f"{ticket_id}.json")
        
        # Skip if already processed
        if os.path.exists(dossier_path):
            continue
            
        print(f"\nJournalist: Investigating Lead '{ticket['title']}'...")
        status_manager.update_agent_status("The Investigative Journalist", "Journalist", "Investigating", f"Interrogating lead: {ticket['title'][:40]}...")
        
        lead = f"Title: {ticket['title']}\nInitial Link: {ticket.get('source_link', 'None')}"

        # --- Step 0: Agentic Thinking (Plan before acting) ---
        print("Journalist: Thinking about the lead...")
        status_manager.update_agent_status("The Investigative Journalist", "Journalist", "Thinking", "Formulating investigation strategy...")
        
        t_sys = prompts.THINKING_PROMPT.replace("{lead}", lead).replace("{date}", time.strftime('%Y-%m-%d'))
        thoughts_data = llm_client.generate_json(t_sys, "Think about this story.")
        
        story_type = thoughts_data.get("story_type", "General News")
        
        # SKIP OLD NEWS
        if "OLD NEWS" in story_type.upper():
            print(f"Journalist: SKIPPING - Detected as Old News. ({story_type})")
            status_manager.update_agent_status("The Investigative Journalist", "Journalist", "Skipping", f"Skipped old news: {ticket['title'][:30]}...")
            # Mark as done so we don't try again immediately? Or just delete?
            # For now, we'll just not create a dossier, effectively skipping it for this run.
            continue

        best_evidence = thoughts_data.get("best_evidence", "Official statements")
        strategy = thoughts_data.get("investigation_strategy", "Search for primary sources")
        
        print(f"Journalist: Strategy -> Find {best_evidence}")

        # --- Step 1: Uncomfortable Questions ---
        print("Journalist: Generating uncomfortable questions...")
        q_sys = prompts.GENERATE_QUESTIONS_PROMPT.replace("{lead}", lead)
        questions_data = llm_client.generate_json(q_sys, "Generate questions now.")
        questions = questions_data.get("questions", []) if questions_data else []
        
        # --- Step 2: Select Angle & Primary Sources ---
        print("Journalist: Selecting angle and primary sources...")
        a_sys = prompts.SELECT_ANGLE_PROMPT.replace("{lead}", lead).replace("{questions}", "\n".join(questions))
        
        # Add context from Thinking step to guide the angle
        a_sys += f"\n\nCONTEXT FROM PLANNING:\nTarget Evidence: {best_evidence}\nStrategy: {strategy}\nUse this to generate BETTER search queries."
        
        angle_data = llm_client.generate_json(a_sys, "Select angle now.")
        
        angle = angle_data.get("angle", "Deep Analysis")
        angle_rationale = angle_data.get("rationale", "")
        primary_queries = angle_data.get("search_queries", [f"{ticket['title']} official statement"])
        
        print(f"Journalist: Angle selected: {angle}")
        
        # --- Step 3: Targeted Search (Primary Sources) ---
        search_results = []
        for query in primary_queries:
            results = search.search_topic(query)
            search_results.extend(results)
            
        # Deduplicate results by URL
        seen_urls = set()
        unique_results = []
        for r in search_results:
            if r['url'] not in seen_urls:
                unique_results.append(r)
                seen_urls.add(r['url'])
        search_results = unique_results[:5] # Keep top 5 most relevant
        
        # --- Step 4: Scrape & Extract Context ---
        facts = []
        quotes = []
        
        for result in search_results:
            url = result['url']
            scrape_data = scraper.scrape_url(url) # returns dict or text
            
            content = ""
            if isinstance(scrape_data, dict):
                content = scrape_data.get('text', '')
            else:
                content = scrape_data
                
            if content:
                # Extract Quotes/Facts via LLM
                e_sys = prompts.EXTRACT_QUOTES_PROMPT.replace("{text}", content[:4000]) # Limit length
                extracted = llm_client.generate_json(e_sys, "Extract quotes and facts.")
                
                if extracted:
                    if extracted.get("quotes"):
                        quotes.extend(extracted["quotes"])
                    if extracted.get("facts"):
                         facts.extend(extracted["facts"])
                
                # Fallback: Just keep a summary if extraction fails or yields nothing
                facts.append(f"Source ({url}): {content[:300]}...")

        # --- Step 5: Negative Space Analysis ---
        print("Journalist: Analyzing negative space...")
        info_summary = "\n".join(facts[:10])
        n_sys = prompts.NEGATIVE_SPACE_PROMPT.replace("{lead}", lead).replace("{info_summary}", info_summary)
        negative_space_data = llm_client.generate_json(n_sys, "Analyze negative space.")
        
        missing_context = negative_space_data.get("missing_context", "")
        follow_up_queries = negative_space_data.get("follow_up_queries", [])
        
        # Optional: Perform follow-up search for negative space (One pass)
        if follow_up_queries:
            print(f"Journalist: Hunting for missing context: {follow_up_queries[0]}...")
            follow_up_results = search.search_topic(follow_up_queries[0])
            if follow_up_results:
                # Quick scrape of top result
                fu_url = follow_up_results[0]['url']
                fu_scrape = scraper.scrape_url(fu_url)
                fu_content = fu_scrape.get('text', '') if isinstance(fu_scrape, dict) else fu_scrape
                if fu_content:
                    facts.append(f"Follow-up Context ({fu_url}): {fu_content[:500]}...")

        # --- Step 5.5: Image Search ---
        print(f"Journalist: Searching for images for '{ticket['title']}'...")
        images = search.search_images(ticket['title'])
        if not images:
             # Fallback to angle if title yields no results
             print(f"Journalist: No images found for title, trying angle '{angle}'...")
             images = search.search_images(angle)
        
        print(f"Journalist: Found {len(images)} images.")

        # --- Step 6: Compile Dossier ---
        dossier = {
            "ticket_id": ticket_id,
            "title": ticket['title'],
            "original_title": ticket['title'],
            "source_link": ticket.get('source_link'),
            "category": ticket.get("category", "Tech"),
            "status": "researched",
            "angle": angle,
            "angle_rationale": angle_rationale,
            "uncomfortable_questions": questions,
            "missing_context": missing_context,
            "key_facts": facts,
            "key_quotes": quotes,
            "images": images,
            "search_results": search_results, # Keep for reference
            "generated_at": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(dossier_path, 'w') as f:
            json.dump(dossier, f, indent=2)
            
        print(f"Journalist: Detailed Dossier saved to {dossier_path}")
        
    print("Journalist: All assignments processed.")
