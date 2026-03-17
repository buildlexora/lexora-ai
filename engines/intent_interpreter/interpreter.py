import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class IntentInterpreter:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def interpret(self, raw_input: str) -> dict:
        prompt = f"""
You are Lexora's Intent Interpreter engine.
Analyze the following idea and return a structured JSON object.

Idea: "{raw_input}"

Return ONLY a valid JSON object with these fields:
{{
  "goal": "clear one line description of what to build",
  "domain": "one of: productivity, ecommerce, social, education, health, finance, general",
  "complexity": "one of: low, medium, high",
  "core_features": ["list", "of", "key", "features"],
  "output_type": "one of: web app, mobile app, api, desktop app",
  "target_users": "who will use this"
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