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
            temperature=0.3,
        )

        raw = response.choices[0].message.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        return json.loads(raw.strip())

    def generate_code(self, intent: dict, architecture: dict) -> dict:
        prompt = f"""
You are Lexora's Code Generator.
Based on the intent and architecture below, generate a complete working codebase.

Intent: {json.dumps(intent, indent=2)}
Architecture: {json.dumps(architecture, indent=2)}

Generate the following files with complete working code:
1. server/index.js — Express server setup
2. server/models/User.js — User model
3. server/routes/index.js — Main routes
4. client/src/App.js — Main React component
5. package.json — Project dependencies
6. .env.example — Environment variables template
7. README.md — Project documentation

Return ONLY a valid JSON object where keys are file paths and values are the complete file contents as strings.
Example format:
{{
  "server/index.js": "const express = require('express')...",
  "server/models/User.js": "const mongoose = require('mongoose')...",
  "client/src/App.js": "import React from 'react'...",
  "package.json": "{{\\"name\\": \\"project\\"...}}",
  ".env.example": "PORT=3000...",
  "README.md": "# Project..."
}}

Return ONLY the JSON. No explanation. No markdown. Generate COMPLETE working code for each file.
"""
        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
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