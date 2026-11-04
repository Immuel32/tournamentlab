import json
from pathlib import Path


class StorageManager:
    """Save and load tournament data using validated JSON."""

    def __init__(self, file_path="data/tournament.json"):
        self.file_path = Path(file_path)

    def validate_data(self, data):
        """Validate the structure and consistency of tournament data."""

        # Validate the top-level structure.
        if not isinstance(data, dict):
            raise ValueError("Invalid tournament data format.")

        if set(data.keys()) != {"teams", "fixtures"}:
            raise ValueError("Tournament data must contain teams and fixtures.")

        teams = data["teams"]
        fixtures = data["fixtures"]

        if not isinstance(teams, list):
            raise ValueError("Teams must be stored as a list.")

        if not isinstance(fixtures, list):
            raise ValueError("Fixtures must be stored as a list.")

        # An entirely empty tournament is valid.
        if not teams and not fixtures:
            return

        # Validate the number of registered teams.
        if not 4 <= len(teams) <= 8:
            raise ValueError("A tournament must have between 4 and 8 teams.")

        # Validate team names.
        normalized_names = set()

        for team in teams:
            if not isinstance(team, str) or not team.strip():
                raise ValueError("Every team must have a valid name.")

            normalized_name = team.strip().casefold()

            if normalized_name in normalized_names:
                raise ValueError("Duplicate team names are not allowed.")

            normalized_names.add(normalized_name)

        # Registered teams without fixtures are allowed.
        if not fixtures:
            return

        expected_fixture_count = len(teams) * (len(teams) - 1) // 2

        if len(fixtures) != expected_fixture_count:
            raise ValueError("Fixture schedule is incomplete or invalid.")

        expected_keys = {
            "id",
            "home_team",
            "away_team",
            "status",
            "home_score",
            "away_score"
        }

        fixture_ids = set()
        pairings = set()

        for fixture in fixtures:

            if not isinstance(fixture, dict):
                raise ValueError("Every fixture must be a dictionary.")

            if set(fixture.keys()) != expected_keys:
                raise ValueError("Fixture contains missing or unexpected fields.")

            fixture_id = fixture["id"]
            home = fixture["home_team"]
            away = fixture["away_team"]
            status = fixture["status"]
            home_score = fixture["home_score"]
            away_score = fixture["away_score"]

            # Validate fixture IDs.
            if (
                isinstance(fixture_id, bool)
                or not isinstance(fixture_id, int)
                or fixture_id < 1
            ):
                raise ValueError("Fixture IDs must be positive integers.")

            if fixture_id in fixture_ids:
                raise ValueError("Duplicate fixture IDs are not allowed.")

            fixture_ids.add(fixture_id)

            # Validate team references.
            if home not in teams or away not in teams:
                raise ValueError("Fixture references an unknown team.")

            if home == away:
                raise ValueError("A team cannot play against itself.")

            # Prevent duplicate pairings in either order.
            pairing = frozenset((home, away))

            if pairing in pairings:
                raise ValueError("Duplicate team pairings are not allowed.")

            pairings.add(pairing)

            # Validate fixture status and scores.
            if status == "pending":

                if home_score is not None or away_score is not None:
                    raise ValueError("Pending fixtures cannot have scores.")

            elif status == "played":

                for score in (home_score, away_score):
                    if (
                        isinstance(score, bool)
                        or not isinstance(score, int)
                        or score < 0
                    ):
                        raise ValueError(
                            "Played fixtures require nonnegative integer scores."
                        )

            else:
                raise ValueError("Fixture status must be pending or played.")

        # IDs must form a continuous sequence starting at 1.
        if fixture_ids != set(range(1, expected_fixture_count + 1)):
            raise ValueError("Fixture IDs must be sequential.")

    def save(self, teams, fixtures):
        """Validate and save tournament data."""

        data = {
            "teams": teams,
            "fixtures": fixtures
        }

        self.validate_data(data)

        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        """Load and validate tournament data."""

        if not self.file_path.exists():
            return {
                "teams": [],
                "fixtures": []
            }

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as error:
            raise ValueError(
                "Tournament data contains invalid JSON."
            ) from error

        except UnicodeDecodeError as error:
            raise ValueError(
                "Tournament data contains invalid text encoding."
            ) from error

        self.validate_data(data)

        return data