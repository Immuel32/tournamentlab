import unittest

from tournament.teams import TeamManager


class TestTeamManager(unittest.TestCase):

    def setUp(self):
        self.manager = TeamManager()

    def test_register_team(self):
        result = self.manager.register_team("Falcons")

        self.assertEqual(result, "Falcons")
        self.assertIn("Falcons", self.manager.teams)

    def test_team_name_is_trimmed(self):
        self.manager.register_team("  Falcons  ")

        self.assertEqual(self.manager.teams, ["Falcons"])

    def test_empty_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.register_team("")

    def test_whitespace_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.register_team("   ")

    def test_non_string_name_is_rejected(self):
        with self.assertRaises(ValueError):
            self.manager.register_team(123)

    def test_duplicate_name_is_rejected(self):
        self.manager.register_team("Falcons")

        with self.assertRaises(ValueError):
            self.manager.register_team("Falcons")

    def test_duplicate_name_ignores_case(self):
        self.manager.register_team("Falcons")

        with self.assertRaises(ValueError):
            self.manager.register_team("FALCONS")

    def test_maximum_eight_teams(self):
        for number in range(8):
            self.manager.register_team(f"Team {number + 1}")

        with self.assertRaises(ValueError):
            self.manager.register_team("Team 9")

    def test_minimum_four_teams(self):
        for number in range(3):
            self.manager.register_team(f"Team {number + 1}")

        with self.assertRaises(ValueError):
            self.manager.validate_team_count()

    def test_four_teams_are_valid(self):
        for number in range(4):
            self.manager.register_team(f"Team {number + 1}")

        self.assertTrue(self.manager.validate_team_count())

    def test_get_teams_returns_copy(self):
        self.manager.register_team("Falcons")

        teams = self.manager.get_teams()
        teams.append("Tigers")

        self.assertEqual(self.manager.teams, ["Falcons"])


if __name__ == "__main__":
    unittest.main()