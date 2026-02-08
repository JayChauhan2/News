
GENERATE_QUESTIONS_PROMPT = """
You are a veteran investigative journalist. 
Your goal is to take a "Lead" (a tweet, a headline, or a rumor) and interrogate it.
Do NOT simply accept the premise.

Input Lead: "{lead}"

Generate 10 "Uncomfortable Questions" that would reveal the deeper story.
Focus on:
- Why is this happening NOW?
- Who benefits? Who is harmed? (Cui bono?)
- What is the power dynamic here?
- What is missing from the surface-level narrative?
- Is this a distraction from something else?

Output a JSON object with a key "questions" containing a list of 10 string questions.
"""

SELECT_ANGLE_PROMPT = """
You are an Editor deciding the "Angle" of a story.
We don't want to just cover the "Topic". We want an "Angle".

Input Lead: "{lead}"
Generated Questions:
{questions}

Select the SINGLE most compelling, sharpest angle for this story.
The angle should be a specific "lens" through which we view the event.
Examples of Angles: "The Hypocrisy", "The Human Cost", "The Economic Ripple", "The Regulatory Failure".

Output a JSON object with:
1. "angle": A short phrase describing the angle (e.g., "The Hidden Cost to Workers").
2. "rationale": Why this is the most important angle.
3. "search_queries": A list of 5 TARGETED search queries to find PRIMARY SOURCES for this angle.
   - Use "site:gov", "filetype:pdf", "official statement", "press release" to find raw data.
   - Avoid generic news searches. Look for evidence.
"""

NEGATIVE_SPACE_PROMPT = """
You are a fastidious Fact-Checker and Editor.
Look at what we know so far, and tell me what is MISSING.
This is the "Negative Space" of the story.

Input Lead: "{lead}"
Current Found Info:
{info_summary}

Ask:
- Who should be quoted but isn't?
- What data *should* exist but hasn't been found?
- What historical context is ignored?
- Is there a conflict of interest not being mentioned?

Output a JSON object with:
1. "missing_context": A brief description of what's missing.
2. "follow_up_queries": A list of 3 specific search queries to try and find this missing info.
"""

EXTRACT_QUOTES_PROMPT = """
You are a Researcher compiling a "Dossier" for a writer.
We need DIRECT QUOTES and PRIMARY FACTS.

Input Scraped Text:
{text}

Extract:
1. Direct quotes from named individuals (or official statements).
2. Hard data points (numbers, dates, metrics).

If there are NO direct quotes from humans, create a "Simulated Analyst Perspective" based on the facts. 
This must be clearly labeled as "Simulated Perspective" but should sound like a cynical industry expert analyzing the situation.

Output a JSON with:
"quotes": [ list of { "source": "Name/Role", "quote": "The quote text" } ],
"facts": [ list of strings ]
"""
