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
You are Lexora's Intent Interpreter — the brain that truly understands what a user wants to build.

Analyze this idea deeply and extract the real intent behind it:
"{raw_input}"

STRICT RULES:
- Read between the lines — understand what the user ACTUALLY needs
- Identify the core problem being solved
- Be specific — "a social app" is not specific enough
- Extract real features based on the idea, not generic ones
- Identify the real target users precisely
- Detect the domain accurately

Return ONLY a valid JSON object:
{{
  "goal": "specific one line description of exactly what to build",
  "problem_being_solved": "what real world problem does this solve",
  "domain": "specific domain (e.g. fintech, edtech, healthtech, ecommerce, social, productivity, entertainment, devtools)",
  "complexity": "one of: simple, moderate, complex, enterprise",
  "core_features": ["specific features based on THIS idea, minimum 5, maximum 10"],
  "nice_to_have_features": ["features that would be great but not essential"],
  "output_type": "one of: static website, web app, mobile app, api, cli tool, data pipeline, ml model, desktop app, browser extension",
  "target_users": "specific description of who will use this",
  "monetization_potential": "one of: free tool, freemium, subscription, marketplace, one-time purchase",
  "similar_products": ["existing products similar to this idea"]
}}

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())