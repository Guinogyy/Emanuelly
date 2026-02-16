import json
import os
import uuid

CONFIG_FILE = "config.json"

class DataManager:
    def __init__(self):
        self.filename = CONFIG_FILE
        self.default_data = {
            "tasks": [],
            "theme": "purple",
            "bias": "V"
        }

    def load_data(self):
        """Loads data from the JSON file. Returns default data if file is missing or invalid."""
        if not os.path.exists(self.filename):
            return self.default_data

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data = json.load(f)

                # Migration: Check if tasks are strings (old format)
                if "tasks" in data and isinstance(data["tasks"], list):
                    if len(data["tasks"]) > 0 and isinstance(data["tasks"][0], str):
                        new_tasks = []
                        for t_str in data["tasks"]:
                            new_tasks.append(self.add_task(t_str))
                        data["tasks"] = new_tasks

                # Ensure all keys exist
                for key, value in self.default_data.items():
                    if key not in data:
                        data[key] = value
                return data
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading data: {e}")
            return self.default_data

    def save_data(self, data):
        """Saves the provided data dictionary to the JSON file."""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except IOError as e:
            print(f"Error saving data: {e}")
            return False

    def add_task(self, text):
        """Helper to create a new task object."""
        return {
            "id": str(uuid.uuid4()),
            "text": text,
            "completed": False
        }
