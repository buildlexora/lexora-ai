from engines.intent_interpreter.interpreter import IntentInterpreter
from engines.system_architect.architect import SystemArchitect
from engines.task_decomposition.decomposer import TaskDecomposer
from engines.execution_engine.executor import ExecutionEngine
from engines.project_state_memory.memory import ProjectStateMemory
from engines.code_quality_guard.guard import CodeQualityGuard
from engines.iteration_engine.iterator import IterationEngine
import json

def main():
    print("⚡ Lexora — Vibe Coding Agent")
    print("------------------------------")
    raw = input("Describe what you want to build: ")

    print("\n🧠 Interpreting intent...")
    interpreter = IntentInterpreter()
    intent = interpreter.interpret(raw)
    print(json.dumps(intent, indent=2))

    print("\n🏗️ Designing architecture...")
    architect = SystemArchitect()
    architecture = architect.design(intent)
    print(json.dumps(architecture, indent=2))

    print("\n📋 Decomposing tasks...")
    decomposer = TaskDecomposer()
    tasks = decomposer.decompose(intent, architecture)
    print(json.dumps(tasks, indent=2))

    print("\n⚙️ Building execution plan...")
    executor = ExecutionEngine()
    execution = executor.execute(intent, architecture, tasks)
    print(json.dumps(execution, indent=2))

    print("\n💾 Saving project state...")
    memory = ProjectStateMemory()
    state = memory.save(intent, architecture, tasks, execution)
    print(json.dumps(memory.get_summary(), indent=2))

    print("\n🛡️ Running quality check...")
    guard = CodeQualityGuard()
    quality = guard.review(intent, architecture, execution)
    print(json.dumps(quality, indent=2))

    print("\n💻 Generating code...")
    print("This may take a moment...\n")
    files = executor.generate_code(intent, architecture)
    written = executor.write_files(files)
    print(f"\n✅ {len(written)} files generated in /output folder!")

    print("\n🔄 Iteration engine ready.")
    feedback = input("Any feedback to refine? (or press Enter to skip): ")
    if feedback.strip():
        iterator = IterationEngine()
        refinements = iterator.refine(state, feedback)
        print("\n✅ Refined Plan:")
        print(json.dumps(refinements, indent=2))

    print("\n⚡ Lexora complete. Build Smarter. Ship Structured.")

if __name__ == "__main__":
    main()