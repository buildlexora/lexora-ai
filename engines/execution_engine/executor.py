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
Based on the intent, architecture and tasks below, generate a detailed execution plan.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}
Tasks: {json.dumps(tasks, indent=2)}

Return ONLY a valid JSON object with these fields:
{{
  "folder_structure": ["list", "of", "folders", "and", "files"],
  "setup_commands": ["list", "of", "terminal", "commands"],
  "first_steps": ["ordered", "list", "of", "first", "things", "to", "code"],
  "key_dependencies": ["list", "of", "packages"],
  "env_variables": ["list", "of", "required", "env", "variables"]
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

    def generate_code(self, intent: dict, architecture: dict, role: dict) -> dict:
        prompt = f"""
You are Lexora's Code Generator. You are a {role.get('primary_role', 'Full Stack Developer')} with 10 years of experience.

Generate a COMPLETE, WORKING, PRODUCTION-READY codebase for this specific project.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}

STRICT RULES:
- Generate code SPECIFIC to this exact project — no generic boilerplate
- Every file must contain REAL, WORKING code for THIS specific app
- Include the actual features listed in the intent
- Use the exact stack specified in the architecture
- If no backend needed, don't generate backend files
- If no database needed, don't generate database files
- Variable names, function names, and logic must match THIS specific project
- A todo app must have todo-specific logic
- A chat app must have chat-specific logic
- A calculator must have calculator-specific logic
- NEVER generate the same generic Express + React template

Generate these files based on what the project actually needs:
- Main entry point
- Core feature files
- UI components specific to this app
- Configuration files
- README specific to this project

Return ONLY a valid JSON object where keys are file paths and values are complete file contents.
Every file must have at least 30 lines of real, working, project-specific code.

Return ONLY the JSON. No explanation. No markdown.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=4000,
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    def write_files(self, files: dict, output_dir: str = "output") -> list:
        os.makedirs(output_dir, exist_ok=True)
        written = []

        for filepath, content in files.items():
            full_path = os.path.join(output_dir, filepath)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "w") as f:
                f.write(content)
            written.append(full_path)
            print(f"  ✅ Created: {full_path}")

        return written