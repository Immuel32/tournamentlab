import json
import tempfile
import unittest
from pathlib import Path

from tournament.storage import StorageManager
from tournament.fixtures import FixtureManager


class TestStorageManager(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.file_path = Path(self.temp_dir.name) / "tournament.json"

        self.storage = StorageManager(self.file_path)

        self.teams = ["Falcons", "Tigers", "Wolves", "Dragons"]

        self.fixtures = FixtureManager().generate_fixtures(self.teams)

        # Record one valid result for storage testing.
        self.fixtures[0]["status"] = "played"
        self.fixtures[0]["home_score"] = 2
        self.fixtures[0]["away_score"] = 1

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_json(self, data):
        """Write test data directly to the temporary JSON file."""
        self.file_path.write_text(
            json.dumps(data),
            encoding="utf-8"
        )

    def valid_data(self):
        return {
            "teams": self.teams.copy(),
            "fixtures": [fixture.copy() for fixture in self.fixtures]
        }

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

    def test_invalid_json_is_rejected(self):
        self.file_path.write_text("{invalid json", encoding="utf-8")

        with self.assertRaises(ValueError):
            self.storage.load()

    def test_invalid_top_level_data_is_rejected(self):
        self.write_json(["Falcons", "Tigers"])

        with self.assertRaises(ValueError):
            self.storage.load()

    def test_missing_data_key_is_rejected(self):
        self.write_json({"teams": self.teams})

        with self.assertRaises(ValueError):
            self.storage.load()

    def test_invalid_team_count_is_rejected(self):
        data = self.valid_data()
        data["teams"] = ["Falcons", "Tigers", "Wolves"]

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_duplicate_team_names_are_rejected(self):
        data = self.valid_data()
        data["teams"] = ["Falcons", "Tigers", "Wolves", "FALCONS"]

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_empty_team_name_is_rejected(self):
        data = self.valid_data()
        data["teams"][0] = "   "

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_fixture_with_unknown_team_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["home_team"] = "Unknown"

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_team_cannot_play_itself(self):
        data = self.valid_data()
        data["fixtures"][0]["away_team"] = "Falcons"

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_duplicate_fixture_id_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][1]["id"] = data["fixtures"][0]["id"]

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_duplicate_pairing_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][1]["home_team"] = "Tigers"
        data["fixtures"][1]["away_team"] = "Falcons"

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_incomplete_fixture_schedule_is_rejected(self):
        data = self.valid_data()
        data["fixtures"].pop()

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_pending_fixture_cannot_have_scores(self):
        data = self.valid_data()
        data["fixtures"][1]["home_score"] = 2

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_negative_score_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["home_score"] = -1

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_boolean_score_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["home_score"] = True

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_invalid_fixture_status_is_rejected(self):
        data = self.valid_data()
        data["fixtures"][0]["status"] = "cancelled"

        with self.assertRaises(ValueError):
            self.storage.validate_data(data)

    def test_registered_teams_without_fixtures_are_valid(self):
        data = {
            "teams": self.teams.copy(),
            "fixtures": []
        }

        self.storage.validate_data(data)

    def test_empty_tournament_is_valid(self):
        self.storage.validate_data({
            "teams": [],
            "fixtures": []
        })


if __name__ == "__main__":
    unittest.main()