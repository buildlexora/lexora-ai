from flask import Flask, request, jsonify
from flask_cors import CORS
from engines.intent_interpreter.interpreter import IntentInterpreter
from engines.system_architect.architect import SystemArchitect
from engines.task_decomposition.decomposer import TaskDecomposer
from engines.execution_engine.executor import ExecutionEngine
from engines.project_state_memory.memory import ProjectStateMemory
from engines.code_quality_guard.guard import CodeQualityGuard
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({"message": "⚡ Lexora API is live. Build Smarter. Ship Structured."})

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

        return jsonify({
            "intent": intent,
            "architecture": architecture,
            "tasks": tasks,
            "execution": execution,
            "summary": summary,
            "quality": quality,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)