import json
from pathlib import Path


class StorageManager:
    """Save and load tournament data using JSON."""

    def __init__(self, file_path="data/tournament.json"):
        self.file_path = Path(file_path)

    def save(self, teams, fixtures):
        """Save teams and fixtures to a JSON file."""

        data = {
            "teams": teams,
            "fixtures": fixtures
        }

        # Create the data directory if it doesn't exist.
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write tournament data as formatted JSON.
        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        """Load tournament data from a JSON file."""

        if not self.file_path.exists():
            return {
                "teams": [],
                "fixtures": []
            }

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError("Tournament data contains invalid JSON.") from error

        # Validate the top-level structure.
        if not isinstance(data, dict):
            raise ValueError("Invalid tournament data format.")

        if set(data.keys()) != {"teams", "fixtures"}:
            raise ValueError("Tournament data must contain teams and fixtures.")

        if not isinstance(data["teams"], list):
            raise ValueError("Teams must be stored as a list.")

        if not isinstance(data["fixtures"], list):
            raise ValueError("Fixtures must be stored as a list.")

        return data