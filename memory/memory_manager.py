import json
import os


class MemoryManager:

    def __init__(self):

        self.memory_path = os.path.join("data", "memory.json")

        if not os.path.exists(self.memory_path):
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump([], f)

        try:
            with open(self.memory_path, "r", encoding="utf-8") as f:
                self.messages = json.load(f)
        except Exception:
            self.messages = []

    def save_memory(self):

        try:
            with open(self.memory_path, "w", encoding="utf-8") as f:
                json.dump(self.messages, f, indent=2)
        except Exception:
            pass

    def add_user_message(self, content):

        self.messages.append({
            "role": "user",
            "content": content
        })

        self.save_memory()

    def add_ai_message(self, content):

        self.messages.append({
            "role": "assistant",
            "content": content
        })

        self.save_memory()

    def get_messages(self):

        limit = 20

        if len(self.messages) > limit:
            return self.messages[-limit:]

        return self.messages