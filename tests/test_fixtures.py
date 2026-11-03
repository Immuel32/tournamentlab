import unittest

from tournament.fixtures import FixtureManager


class TestFixtureManager(unittest.TestCase):

    def setUp(self):
        """Create a fresh fixture manager before each test."""
        self.manager = FixtureManager()

    def test_four_teams_generate_six_fixtures(self):
        teams = ["red", "blue", "green", "yellow"]

        fixtures = self.manager.generate_fixtures(teams)

        self.assertEqual(len(fixtures), 6)

    def test_three_teams_generate_three_fixtures(self):
        teams = ["red", "blue", "green"]

        fixtures = self.manager.generate_fixtures(teams)

        self.assertEqual(len(fixtures), 3)

    def test_fixture_ids_are_unique(self):
        teams = ["red", "blue", "green", "yellow"]

        fixtures = self.manager.generate_fixtures(teams)

        fixture_ids = [fixture["id"] for fixture in fixtures]

        self.assertEqual(len(fixture_ids), len(set(fixture_ids)))

    def test_team_does_not_play_itself(self):
        teams = ["red", "blue", "green", "yellow"]

        fixtures = self.manager.generate_fixtures(teams)

        for fixture in fixtures:
            self.assertNotEqual(
                fixture["home_team"],
                fixture["away_team"]
            )

    def test_no_duplicate_fixtures(self):
        teams = ["red", "blue", "green", "yellow"]

        fixtures = self.manager.generate_fixtures(teams)

        # Sort each pair so Red vs Blue equals Blue vs Red.
        pairs = [
            tuple(sorted((fixture["home_team"], fixture["away_team"])))
            for fixture in fixtures
        ]

        self.assertEqual(len(pairs), len(set(pairs)))

    def test_new_fixtures_have_pending_status_and_no_scores(self):
        teams = ["red", "blue", "green", "yellow"]

        fixtures = self.manager.generate_fixtures(teams)

        for fixture in fixtures:
            self.assertEqual(fixture["status"], "pending")
            self.assertIsNone(fixture["home_score"])
            self.assertIsNone(fixture["away_score"])


if __name__ == "__main__":
    unittest.main()