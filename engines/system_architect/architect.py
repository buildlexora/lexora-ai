import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class SystemArchitect:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def design(self, intent: dict, role: dict) -> dict:
        prompt = f"""
You are Lexora's System Architect. You think like a senior developer with 10 years of experience.

Based on the intent and role detection below, design the most appropriate system architecture.
Only include components that are actually needed for this specific project.

Intent: {json.dumps(intent, indent=2)}
Role Detection: {json.dumps(role, indent=2)}

STRICT RULES:
- If requires_backend is false, do NOT include a backend
- If requires_database is false, do NOT include a database
- If project_type is static website, only include frontend and hosting
- Choose the most appropriate technology for THIS specific project, not a generic stack
- A simple calculator does not need MongoDB
- A landing page does not need Node.js
- A chat app needs websockets
- A data project needs Python not React

Return ONLY a valid JSON object:
{{
  "components": ["only the components this app actually needs"],
  "stack": {{
    "include only relevant keys from: frontend, backend, database, hosting, realtime, ml_framework, mobile"
  }},
  "recommended_stack": {{
    "same structure as stack but with your top recommendation"
  }},
  "alternative_stacks": [
    {{"name": "alternative option name", "stack": {{}}}}
  ],
  "core_modules": ["specific modules for THIS app"],
  "api_endpoints": ["only if backend exists"],
  "database_models": ["only if database exists"],
  "estimated_build_time": "realistic estimate",
  "why_this_stack": "one sentence explaining why this stack fits this specific project"
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