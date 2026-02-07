from backend import llm_client
import json

existing = [
    "Pelosi's Power Play: Why the Former Speaker Is Betting on a Kennedy in New York"
]

new_title = "Pelosi's Power Play: The Kennedy Comeback Kid Gets Her Blessing"

prompt = f"""
You are a smart News Editor. 
Determine if the NEW HEADLINE is reporting on the SAME SPECIFIC EVENT as any of the EXISTING HEADLINES.

NEW HEADLINE: "{new_title}"

EXISTING HEADLINES:
{json.dumps(existing, indent=2)}

Rules:
- "Same event" means they cover the same core duplicate story (e.g. "Earthquake in Japan" vs "7.0 Magnitude Quake hits Tokyo").
- If matches, return the EXACT/IDENTICAL duplicate headline from the list.
- If no match, return "None".
- Output only the string of the matching headline or "None".
"""

print("Prompting LLM...")
try:
    result = llm_client.generate_json("You output a JSON with key 'match' which is the string or null.", prompt)
    print("Result:", result)
except Exception as e:
    print("Error:", e)
