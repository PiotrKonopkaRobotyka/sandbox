import json
import os

def load_config(file_path):
    """Load configuration from a JSON file safely."""
    if not os.path.exists(file_path):
        # Lepiej rzucić wyjątek, żeby main.py wiedział, że jest źle
        raise FileNotFoundError(f"Config file missing: {file_path}")

    print(f"Loading configuration from: {file_path}")

    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
            return config
    except json.JSONDecodeError as e:
        # Tutaj logujemy błąd struktury JSON
        print(f"ERROR: Corrupted config file! Details: {e}")
        return None  # Lub rzuć wyjątek dalej
