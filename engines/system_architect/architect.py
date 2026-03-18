import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SystemArchitect:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def design(self, intent: dict) -> dict:
        prompt = f"""
You are Lexora's System Architect engine.
Based on the following structured intent, design a complete system architecture.

Intent: {json.dumps(intent, indent=2)}

Return ONLY a valid JSON object with these fields:
{{
  "stack": {{
    "frontend": "technology name",
    "backend": "technology name",
    "database": "technology name",
    "hosting": "technology name"
  }},
  "layers": ["list", "of", "architecture", "layers"],
  "core_modules": ["list", "of", "core", "modules", "to", "build"],
  "api_endpoints": ["list", "of", "key", "api", "endpoints"],
  "database_models": ["list", "of", "main", "database", "models"],
  "estimated_build_time": "realistic estimate like 2-3 weeks"
}}

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        raw = response.choices[0].message.content.strip()
        return json.loads(raw)