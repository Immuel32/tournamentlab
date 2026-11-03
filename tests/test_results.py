import unittest

from tournament.results import find_fixture, record_result


class TestResultManager(unittest.TestCase):

    def setUp(self):
        """Create fresh fixtures before each test."""
        self.fixtures = [
            {
                "id": 1,
                "home_team": "red",
                "away_team": "blue",
                "status": "pending",
                "home_score": None,
                "away_score": None
            },
            {
                "id": 2,
                "home_team": "red",
                "away_team": "green",
                "status": "pending",
                "home_score": None,
                "away_score": None
            }
        ]

    def test_find_existing_fixture(self):
        fixture = find_fixture(self.fixtures, 1)
        self.assertEqual(fixture["id"], 1)

    def test_find_nonexistent_fixture(self):
        fixture = find_fixture(self.fixtures, 10)
        self.assertIsNone(fixture)

    def test_record_valid_result(self):
        fixture = record_result(self.fixtures, 1, 3, 1)

        self.assertEqual(fixture["home_score"], 3)
        self.assertEqual(fixture["away_score"], 1)
        self.assertEqual(fixture["status"], "played")

    def test_record_zero_zero_draw(self):
        fixture = record_result(self.fixtures, 1, 0, 0)

        self.assertEqual(fixture["home_score"], 0)
        self.assertEqual(fixture["away_score"], 0)
        self.assertEqual(fixture["status"], "played")

    def test_reject_nonexistent_fixture(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 10, 2, 1)

    def test_reject_duplicate_result(self):
        record_result(self.fixtures, 1, 3, 1)

        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, 2, 0)

    def test_reject_negative_home_score(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, -1, 2)

    def test_reject_negative_away_score(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, 2, -1)

    def test_reject_non_integer_home_score(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, 2.5, 1)

    def test_reject_non_integer_away_score(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, 2, "1")

    def test_reject_boolean_scores(self):
        with self.assertRaises(ValueError):
            record_result(self.fixtures, 1, True, 1)


if __name__ == "__main__":
    unittest.main()