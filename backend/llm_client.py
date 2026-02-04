import os
import json
import time
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configuration
PROVIDER = os.getenv("LLM_PROVIDER", "openrouter")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Clients
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
) if OPENROUTER_API_KEY else None

# Free Model (Gemini Flash Lite 2.0 Preview)
MODEL_NAME = "arcee-ai/trinity-large-preview:free"

def generate_json(system_prompt, user_prompt, temperature=0.7, retries=3):
    """
    Generates a JSON response using OpenRouter (OpenAI-compatible).
    """
    if not client:
        print("Warning: OPENROUTER_API_KEY not found.")
        return None

    # Throttling to be safe, though free tier usually handles standard traffic
    time.sleep(2)

    for attempt in range(retries):
        try:
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": system_prompt + "\nYou helpfully output valid JSON."},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature,
                # OpenRouter usually maps response_format to the underlying model
                # But 'json_object' mode depends on the specific model support.
                # We'll omit strictly enforcing it via API param to be safe with all models, 
                # relying on the system prompt instruction.
                # response_format={"type": "json_object"} 
            )
            
            content = completion.choices[0].message.content
            
            # Clean markdown if present
            content = content.replace("```json", "").replace("```", "").strip()
            
            # Simple sanitization for common control char issues
            # Verify if it works; if not, we fallback to printing raw for debug
            try:
                return json.loads(content, strict=False)
            except json.JSONDecodeError as e:
                print(f"JSON Parse Error: {e}")
                print(f"Raw Content: {content[:500]}...") # Print first 500 chars
                # Attempt to escape newlines if that's the issue (naive fix)
                try:
                    import re
                    # basic attempt to fix unescaped newlines inside strings might be hard without regex
                    # for now, just retry or fail gracefully
                    return None
                except:
                    return None
            
        except Exception as e:
            print(f"OpenRouter Error (Attempt {attempt+1}/{retries}): {e}")
            time.sleep(5)
    
    print("OpenRouter: Max retries exceeded.")
    return None
