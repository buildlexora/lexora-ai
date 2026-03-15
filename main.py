from engines.intent_interpreter.interpreter import IntentInterpreter
import json

def main():
    print("⚡ Lexora — Intent Interpreter")
    print("--------------------------------")
    raw = input("Describe what you want to build: ")
    
    interpreter = IntentInterpreter()
    result = interpreter.interpret(raw)
    
    print("\n✅ Structured Intent:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()