from engines.intent_interpreter.interpreter import IntentInterpreter
from engines.system_architect.architect import SystemArchitect
import json

def main():
    print("⚡ Lexora — Intent to Architecture")
    print("------------------------------------")
    raw = input("Describe what you want to build: ")
    
    interpreter = IntentInterpreter()
    intent = interpreter.interpret(raw)
    
    print("\n✅ Structured Intent:")
    print(json.dumps(intent, indent=2))

    architect = SystemArchitect()
    architecture = architect.design(intent)
    
    print("\n🏗️ System Architecture:")
    print(json.dumps(architecture, indent=2))

if __name__ == "__main__":
    main()