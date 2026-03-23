from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from engines.intent_interpreter.interpreter import IntentInterpreter
from engines.system_architect.architect import SystemArchitect
from engines.task_decomposition.decomposer import TaskDecomposer
from engines.execution_engine.executor import ExecutionEngine
from engines.project_state_memory.memory import ProjectStateMemory
from engines.code_quality_guard.guard import CodeQualityGuard
import os
import zipfile
import io

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)

@app.route('/')
def home():
    return app.send_static_file('index.html')

@app.route('/build', methods=['POST'])
def build():
    data = request.json
    raw = data.get('idea', '')

    if not raw:
        return jsonify({"error": "No idea provided"}), 400

    try:
        interpreter = IntentInterpreter()
        intent = interpreter.interpret(raw)

        architect = SystemArchitect()
        architecture = architect.design(intent)

        decomposer = TaskDecomposer()
        tasks = decomposer.decompose(intent, architecture)

        executor = ExecutionEngine()
        execution = executor.execute(intent, architecture, tasks)

        memory = ProjectStateMemory()
        state = memory.save(intent, architecture, tasks, execution)
        summary = memory.get_summary()

        guard = CodeQualityGuard()
        quality = guard.review(intent, architecture, execution)

        print("💻 Generating code...")
        files = executor.generate_code(intent, architecture)

        return jsonify({
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