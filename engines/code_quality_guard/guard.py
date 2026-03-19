import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CodeQualityGuard:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def review(self, intent: dict, architecture: dict, execution: dict) -> dict:
        prompt = f"""
You are Lexora's Code Quality Guard engine.
Review the following project plan and identify potential issues, risks and improvements.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}
Execution Plan: {json.dumps(execution, indent=2)}

Return ONLY a valid JSON object with these fields:
{{
  "quality_score": "score out of 10",
  "risks": ["list", "of", "potential", "risks"],
  "improvements": ["list", "of", "suggested", "improvements"],
  "security_concerns": ["list", "of", "security", "issues", "to", "address"],
  "scalability_notes": ["list", "of", "scalability", "considerations"],
  "approved": true or false
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