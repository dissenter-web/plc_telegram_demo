import json
import os
from datetime import datetime


class Storage:
    def __init__(self, path):
        self.path = path
        self._ensure_file()

    def _ensure_file(self):
        # создаёт папку (например data/)
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                json.dump({
                    "active_chat_id": None,
                    "events": []
                }, f)

    def read(self):
        with open(self.path) as f:
            return json.load(f)

    def write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def set_active_chat(self, chat_id):
        data = self.read()
        data["active_chat_id"] = chat_id
        self.write(data)

    def get_active_chat(self):
        return self.read().get("active_chat_id")

    def add_event(self, event_type, label):
        data = self.read()

        event = {
            "event_type": event_type,
            "label": label,
            "created_at": datetime.now().isoformat()
        }

        data["events"].append(event)

        # оставляем только последние 100 событий
        data["events"] = data["events"][-100:]

        self.write(data)
        return event

    def get_events(self):
        return self.read().get("events", [])
                                            