import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class TaskDecomposer:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def decompose(self, intent: dict, architecture: dict) -> dict:
        prompt = f"""
You are Lexora's Task Decomposition engine.
Based on the intent and architecture below, break the project into actionable tasks.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}

Return ONLY a valid JSON object with these fields:
{{
  "phases": [
    {{
      "phase": "phase name",
      "duration": "estimated duration",
      "tasks": [
        {{
          "task": "task name",
          "priority": "high/medium/low",
          "estimated_time": "time estimate"
        }}
      ]
    }}
  ],
  "total_estimated_time": "total project duration",
  "recommended_team_size": "number of developers"
}}

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )

        from engines.utils import clean_and_parse
        raw = response.choices[0].message.content
        return clean_and_parse(raw)