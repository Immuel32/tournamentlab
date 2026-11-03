import unittest

from tournament.standings import (
    initialize_standings,
    calculate_standings
)


class TestStandings(unittest.TestCase):

    def setUp(self):
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
                "home_team": "green",
                "away_team": "red",
                "status": "played",
                "home_score": 2,
                "away_score": 2
            },
            {
                "id": 3,
                "home_team": "blue",
                "away_team": "green",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_initialize_standings(self):
        standings = initialize_standings(self.teams)

        self.assertEqual(len(standings), 3)
        self.assertEqual(standings["red"]["points"], 0)

    def test_calculate_matches_played(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["played"], 2)
        self.assertEqual(standings["blue"]["played"], 1)

    def test_calculate_wins(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["wins"], 1)

    def test_calculate_draws(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["draws"], 1)
        self.assertEqual(standings["green"]["draws"], 1)

    def test_calculate_goals(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["goals_for"], 5)
        self.assertEqual(standings["red"]["goals_against"], 3)

    def test_calculate_goal_difference(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["goal_difference"], 2)

    def test_calculate_points(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["red"]["points"], 4)
        self.assertEqual(standings["blue"]["points"], 0)
        self.assertEqual(standings["green"]["points"], 1)

    def test_pending_fixtures_are_ignored(self):
        standings = dict(calculate_standings(self.teams, self.fixtures))

        self.assertEqual(standings["blue"]["played"], 1)

    def test_teams_are_ranked_correctly(self):
        standings = calculate_standings(self.teams, self.fixtures)

        self.assertEqual(standings[0][0], "red")
        self.assertEqual(standings[1][0], "green")
        self.assertEqual(standings[2][0], "blue")


if __name__ == "__main__":
    unittest.main()