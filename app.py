from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from engines.role_detector.detector import RoleDetector
from engines.intent_interpreter.interpreter import IntentInterpreter
from engines.system_architect.architect import SystemArchitect
from engines.task_decomposition.decomposer import TaskDecomposer
from engines.execution_engine.executor import ExecutionEngine
from engines.project_state_memory.memory import ProjectStateMemory
from engines.code_quality_guard.guard import CodeQualityGuard
import os
import zipfile
import io
import json

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/build', methods=['POST'])
def build():
    data = request.json
    raw = data.get('idea', '')
    user_stack = data.get('user_stack', None)

    if not raw:
        return jsonify({"error": "No idea provided"}), 400

    try:
        detector = RoleDetector()
        role = detector.detect(raw)

        interpreter = IntentInterpreter()
        intent = interpreter.interpret(raw)

        architect = SystemArchitect()
        architecture = architect.design(intent, role)

        if user_stack:
            architecture['stack'] = user_stack

        decomposer = TaskDecomposer()
        tasks = decomposer.decompose(intent, architecture)

        executor = ExecutionEngine()
        execution = executor.execute(intent, architecture, tasks)

        memory = ProjectStateMemory()
        state = memory.save(intent, architecture, tasks, execution)
        summary = memory.get_summary()

        files = executor.generate_code(intent, architecture, role)

        guard = CodeQualityGuard()
        quality = guard.review(intent, architecture, files)

        return jsonify({
            "role": role,
            "intent": intent,
            "architecture": architecture,
            "tasks": tasks,
            "execution": execution,
            "summary": summary,
            "quality": quality,
            "files": files,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/improve', methods=['POST'])
def improve():
    data = request.json
    idea = data.get('idea', '')
    feedback = data.get('feedback', '')
    current_files = data.get('current_files', {})
    current_intent = data.get('current_intent', {})
    current_architecture = data.get('current_architecture', {})

    if not feedback:
        return jsonify({"error": "No feedback provided"}), 400

    try:
        executor = ExecutionEngine()
        
        prompt = f"""
You are Lexora's Iteration Engine improving an existing project.

Original Project: {json.dumps(current_intent, indent=2)}
Current Architecture: {json.dumps(current_architecture, indent=2)}
User Feedback: "{feedback}"

Current files:
{json.dumps({k: v[:500] for k, v in current_files.items()}, indent=2)}

STRICT RULES:
- Do NOT create a new project
- Improve the EXISTING code based on feedback
- Keep what's working, fix what's not
- Apply the specific improvements the user requested
- Return the same file structure with improved code

Return ONLY a valid JSON object where keys are file paths and values are improved file contents.
Return ONLY the JSON. No explanation. No markdown.
"""
        response = executor.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=4000,
        )

        from engines.utils import clean_and_parse
        raw = response.choices[0].message.content
        improved_files = clean_and_parse(raw)

        guard = CodeQualityGuard()
        quality = guard.review(current_intent, current_architecture, improved_files)

        return jsonify({
            "files": improved_files,
            "quality": quality,
            "message": "Code improved based on your feedback"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    files = data.get('files', {})

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for filepath, content in files.items():
            zip_file.writestr(filepath, content)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        mimetype='application/zip',
        as_attachment=True,
        download_name='lexora-project.zip'
    )

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)