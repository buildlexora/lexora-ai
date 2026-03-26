import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class CodeQualityGuard:
    def __init__(self):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    def review(self, intent: dict, architecture: dict, files: dict) -> dict:
        code_summary = ""
        for filepath, content in files.items():
            code_summary += f"\n--- {filepath} ---\n{content[:500]}\n"

        prompt = f"""
You are Lexora's Code Quality Guard — a senior code reviewer with 10 years of experience.
You are reviewing ACTUAL generated code, not a plan.

Project Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}

Generated Code Sample:
{code_summary}

Analyze this code CRITICALLY and HONESTLY. Do not give high scores to bad code.
Check for:
- Is the code actually specific to this project or is it generic boilerplate?
- Are the features from the intent actually implemented?
- Is there proper error handling?
- Are there security vulnerabilities?
- Is the code structure clean and maintainable?
- Are there missing critical files?
- Is the code production ready?

Return ONLY a valid JSON object:
{{
  "quality_score": "honest score out of 10 based on actual code quality",
  "is_project_specific": true or false,
  "features_implemented": ["list of features that are actually implemented"],
  "features_missing": ["list of features from intent that are NOT implemented"],
  "risks": ["real risks found in the actual code"],
  "improvements": ["specific improvements needed for THIS code"],
  "security_concerns": ["actual security issues found in the code"],
  "scalability_notes": ["scalability issues specific to this codebase"],
  "approved": true or false,
  "verdict": "one honest sentence about the overall code quality"
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