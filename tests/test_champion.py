import unittest

from tournament.champion import determine_champion


class TestChampion(unittest.TestCase):

    def setUp(self):
        """Create sample teams and fixtures for testing."""

        self.teams = ["red", "blue", "green"]

        self.fixtures = [
            {
                "id": 1,
                "home_team": "red",
                "away_team": "blue",
                "status": "played",
                "home_score": 3,
                "away_score": 1
            },
            {
                "id": 2,
                "home_team": "red",
                "away_team": "green",
                "status": "played",
                "home_score": 2,
                "away_score": 0
            },
            {
                "id": 3,
                "home_team": "blue",
                "away_team": "green",
                "status": "played",
                "home_score": 1,
                "away_score": 1
            }
        ]

    def test_champion_when_all_fixtures_are_completed(self):
        champion = determine_champion(self.teams, self.fixtures)

        self.assertEqual(champion, "red")

    def test_no_champion_when_fixture_is_pending(self):
        self.fixtures[2]["status"] = "pending"
        self.fixtures[2]["home_score"] = None
        self.fixtures[2]["away_score"] = None

        champion = determine_champion(self.teams, self.fixtures)

        self.assertIsNone(champion)

    def test_no_champion_when_top_position_is_tied(self):
        teams = ["red", "blue"]

        fixtures = [
            {
                "id": 1,
                "home_team": "red",
                "away_team": "blue",
                "status": "played",
                "home_score": 1,
                "away_score": 1
            }
        ]

        champion = determine_champion(teams, fixtures)

        self.assertIsNone(champion)

    def test_no_champion_when_there_are_no_fixtures(self):
        champion = determine_champion(self.teams, [])

        self.assertIsNone(champion)


if __name__ == "__main__":
    unittest.main()