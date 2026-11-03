import unittest

from tournament.simulation import simulate_fixture


class TestSimulation(unittest.TestCase):

    def setUp(self):
        self.fixtures = [
            {
                "id": 1,
                "home_team": "Falcons",
                "away_team": "Tigers",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_simulation_records_result(self):
        result = simulate_fixture(self.fixtures, 1, 42)

        self.assertEqual(result["status"], "played")
        self.assertIsInstance(result["home_score"], int)
        self.assertIsInstance(result["away_score"], int)

    def test_simulation_scores_are_nonnegative(self):
        result = simulate_fixture(self.fixtures, 1, 42)

        self.assertGreaterEqual(result["home_score"], 0)
        self.assertGreaterEqual(result["away_score"], 0)

    def test_same_seed_produces_same_result(self):
        first_fixtures = [fixture.copy() for fixture in self.fixtures]
        second_fixtures = [fixture.copy() for fixture in self.fixtures]

        first = simulate_fixture(first_fixtures, 1, 42)
        second = simulate_fixture(second_fixtures, 1, 42)

        self.assertEqual(
            first["home_score"],
            second["home_score"]
        )
        self.assertEqual(
            first["away_score"],
            second["away_score"]
        )

    def test_missing_fixture_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_fixture(self.fixtures, 99, 42)

    def test_invalid_seed_is_rejected(self):
        with self.assertRaises(ValueError):
            simulate_fixture(self.fixtures, 1, "invalid")

    def test_already_played_fixture_cannot_be_simulated(self):
        simulate_fixture(self.fixtures, 1, 42)

        with self.assertRaises(ValueError):
            simulate_fixture(self.fixtures, 1, 42)


if __name__ == "__main__":
    unittest.main()