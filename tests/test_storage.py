import json
import tempfile
import unittest
from pathlib import Path

from tournament.storage import StorageManager


class TestStorageManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "tournament.json"

        self.storage = StorageManager(self.file_path)

        self.teams = ["red", "blue"]

        self.fixtures = [
            {
                "id": 1,
                "home_team": "red",
                "away_team": "blue",
                "status": "played",
                "home_score": 2,
                "away_score": 1
            }
        ]

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_creates_json_file(self):
        self.storage.save(self.teams, self.fixtures)

        self.assertTrue(self.file_path.exists())

    def test_load_saved_tournament(self):
        self.storage.save(self.teams, self.fixtures)

        data = self.storage.load()

        self.assertEqual(data["teams"], self.teams)
        self.assertEqual(data["fixtures"], self.fixtures)

    def test_missing_file_returns_empty_tournament(self):
        data = self.storage.load()

        self.assertEqual(data["teams"], [])
        self.assertEqual(data["fixtures"], [])

    def test_invalid_json_raises_value_error(self):
        self.file_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            self.storage.load()

    def test_invalid_top_level_data_is_rejected(self):
        self.file_path.write_text(
            json.dumps(["red", "blue"]),
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            self.storage.load()

    def test_missing_data_key_is_rejected(self):
        self.file_path.write_text(
            json.dumps({"teams": ["red"]}),
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            self.storage.load()


if __name__ == "__main__":
    unittest.main()