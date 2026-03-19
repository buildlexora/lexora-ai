import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class IterationEngine:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def refine(self, state: dict, feedback: str) -> dict:
        prompt = f"""
You are Lexora's Iteration Engine.
Based on the current project state and user feedback, suggest refinements and improvements.

Current State: {json.dumps(state, indent=2)}
User Feedback: "{feedback}"

Return ONLY a valid JSON object with these fields:
{{
  "refinements": ["list", "of", "suggested", "refinements"],
  "updated_priorities": ["list", "of", "reprioritized", "tasks"],
  "new_features": ["list", "of", "new", "features", "to", "consider"],
  "removed_features": ["list", "of", "features", "to", "cut"],
  "next_action": "the single most important thing to do next"
}}

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        raw = response.choices[0].message.content.strip()
        
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        
        return json.loads(raw.strip())