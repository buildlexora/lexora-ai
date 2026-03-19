import os
import json
from datetime import datetime

class ProjectStateMemory:
    def __init__(self):
        self.state = {}

    def save(self, intent: dict, architecture: dict, tasks: dict, execution: dict) -> dict:
        self.state = {
            "project_id": f"lexora_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "created_at": datetime.now().isoformat(),
            "status": "active",
            "intent": intent,
            "architecture": architecture,
            "tasks": tasks,
            "execution": execution,
            "progress": {
                "total_phases": len(tasks.get("phases", [])),
                "completed_phases": 0,
                "current_phase": tasks.get("phases", [{}])[0].get("phase", "Not started"),
            }
        }
        return self.state

    def update_progress(self, completed_phases: int) -> dict:
        self.state["progress"]["completed_phases"] = completed_phases
        total = self.state["progress"]["total_phases"]
        self.state["progress"]["completion_percentage"] = round((completed_phases / total) * 100) if total > 0 else 0
        return self.state

    def get_summary(self) -> dict:
        return {
            "project_id": self.state.get("project_id"),
            "status": self.state.get("status"),
            "goal": self.state.get("intent", {}).get("goal"),
            "progress": self.state.get("progress"),
            "created_at": self.state.get("created_at"),
        }