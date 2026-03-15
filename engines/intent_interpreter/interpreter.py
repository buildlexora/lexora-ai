class IntentInterpreter:
    def __init__(self):
        self.domain_keywords = {
            "productivity": ["task", "habit", "track", "schedule"],
            "ecommerce": ["shop", "buy", "sell", "product"],
            "social": ["connect", "share", "follow", "post"],
            "education": ["learn", "study", "course", "quiz"],
        }

    def interpret(self, raw_input: str) -> dict:
        return {
            "goal": self.extract_goal(raw_input),
            "domain": self.detect_domain(raw_input),
            "complexity": self.estimate_complexity(raw_input),
            "core_features": self.extract_features(raw_input),
            "output_type": self.detect_output_type(raw_input),
        }

    def detect_domain(self, text: str) -> str:
        text = text.lower()
        for domain, keywords in self.domain_keywords.items():
            if any(kw in text for kw in keywords):
                return domain
        return "general"

    def extract_goal(self, text: str) -> str:
        return text.strip().lower()

    def estimate_complexity(self, text: str) -> str:
        word_count = len(text.split())
        if word_count < 10:
            return "low"
        elif word_count < 25:
            return "medium"
        return "high"

    def extract_features(self, text: str) -> list:
        return []

    def detect_output_type(self, text: str) -> str:
        text = text.lower()
        if any(w in text for w in ["app", "mobile", "android", "ios"]):
            return "mobile app"
        if any(w in text for w in ["website", "web", "browser"]):
            return "web app"
        if any(w in text for w in ["api", "backend", "server"]):
            return "api"
        return "web app"