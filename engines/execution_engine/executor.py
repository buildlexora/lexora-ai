import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class ExecutionEngine:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def execute(self, intent: dict, architecture: dict, tasks: dict) -> dict:
        prompt = f"""
You are Lexora's Execution Engine.
Based on the intent, architecture and tasks below, generate a detailed execution plan with code structure.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}
Tasks: {json.dumps(tasks, indent=2)}

Return ONLY a valid JSON object with these fields:
{{
  "folder_structure": ["list", "of", "folders", "and", "files"],
  "setup_commands": ["list", "of", "terminal", "commands", "to", "setup", "project"],
  "first_steps": ["ordered", "list", "of", "first", "things", "to", "code"],
  "key_dependencies": ["list", "of", "npm", "or", "pip", "packages"],
  "env_variables": ["list", "of", "required", "environment", "variables"]
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