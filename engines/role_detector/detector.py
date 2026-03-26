import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class RoleDetector:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def detect(self, raw_input: str) -> dict:
        prompt = f"""
You are Lexora's Role Detector — the first and most critical engine.
Analyze the following project idea and determine exactly what kind of development is needed.

Project idea: "{raw_input}"

Think deeply about what this project actually needs. Not every app needs a backend. Not every project needs a database. Be smart and specific.

Return ONLY a valid JSON object with these fields:
{{
  "primary_role": "the main developer role needed (e.g. Frontend Developer, Full Stack Developer, Backend Developer, Mobile Developer, Data Engineer, DevOps Engineer, ML Engineer)",
  "secondary_roles": ["list of other roles needed if any"],
  "requires_backend": true or false,
  "requires_database": true or false,
  "requires_authentication": true or false,
  "requires_realtime": true or false,
  "requires_payments": true or false,
  "requires_ml": true or false,
  "requires_mobile": true or false,
  "requires_devops": true or false,
  "project_type": "one of: static website, web app, mobile app, api, cli tool, data pipeline, ml model, desktop app, browser extension",
  "complexity": "one of: simple, moderate, complex, enterprise",
  "reasoning": "one sentence explaining why you chose these roles and components"
}}

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        from engines.utils import clean_and_parse
        raw = response.choices[0].message.content
        return clean_and_parse(raw)