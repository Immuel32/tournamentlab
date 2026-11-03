class FixtureManager:
    """Generate and manage tournament fixtures."""

    def generate_fixtures(self, teams):
        """Generate a single round-robin schedule."""

        fixtures = []

        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):

                fixture = {
                    "id": len(fixtures) + 1,
                    "home_team": teams[i],
                    "away_team": teams[j],
                    "status": "pending",
                    "home_score": None,
                    "away_score": None
                }

                fixtures.append(fixture)

        return fixtures