def find_fixture(fixtures, fixture_id):
    """Find a fixture using its unique ID."""

    for fixture in fixtures:
        if fixture["id"] == fixture_id:
            return fixture

    return None


def record_result(fixtures, fixture_id, home_score, away_score):
    """Record a valid result for a scheduled fixture."""

    # Find the fixture using its ID.
    fixture = find_fixture(fixtures, fixture_id)

    # Reject a fixture that does not exist.
    if fixture is None:
        raise ValueError("Fixture not found.")

    # Prevent duplicate result submissions.
    if fixture["status"] == "played":
        raise ValueError("This fixture has already been played.")

    # Validate scores: they must be integers, not booleans.
    if (
        isinstance(home_score, bool)
        or not isinstance(home_score, int)
        or isinstance(away_score, bool)
        or not isinstance(away_score, int)
    ):
        raise ValueError("Scores must be integers.")

    # Scores cannot be negative.
    if home_score < 0 or away_score < 0:
        raise ValueError("Scores cannot be negative.")

    # Update the fixture after all validation succeeds.
    fixture["home_score"] = home_score
    fixture["away_score"] = away_score
    fixture["status"] = "played"

    return fixture