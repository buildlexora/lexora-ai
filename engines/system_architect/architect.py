class SystemArchitect:
    def __init__(self):
        self.architecture_templates = {
            "web app": {
                "frontend": "React.js",
                "backend": "Node.js + Express",
                "database": "MongoDB",
                "hosting": "Vercel + Railway",
            },
            "mobile app": {
                "frontend": "React Native",
                "backend": "Node.js + Express",
                "database": "Firebase",
                "hosting": "Expo + Railway",
            },
            "api": {
                "frontend": None,
                "backend": "FastAPI (Python)",
                "database": "PostgreSQL",
                "hosting": "Railway",
            },
        }

        self.domain_features = {
            "productivity": ["user auth", "dashboard", "data tracking", "notifications"],
            "ecommerce": ["user auth", "product listing", "cart", "payments", "orders"],
            "social": ["user auth", "profiles", "feed", "messaging", "notifications"],
            "education": ["user auth", "course listing", "progress tracking", "quizzes"],
            "general": ["user auth", "dashboard", "CRUD operations"],
        }

    def design(self, intent: dict) -> dict:
        output_type = intent.get("output_type", "web app")
        domain = intent.get("domain", "general")

        stack = self.architecture_templates.get(output_type, self.architecture_templates["web app"])
        features = self.domain_features.get(domain, self.domain_features["general"])

        return {
            "output_type": output_type,
            "domain": domain,
            "stack": stack,
            "core_features": features,
            "layers": self.define_layers(output_type),
        }

    def define_layers(self, output_type: str) -> list:
        if output_type == "api":
            return ["API Layer", "Business Logic Layer", "Data Layer"]
        return ["Presentation Layer", "Business Logic Layer", "Data Layer", "Infrastructure Layer"]