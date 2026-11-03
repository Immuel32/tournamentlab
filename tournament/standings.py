def initialize_standings(teams):
    """Create an initial standings record for every team."""

    standings = {}

    for team in teams:
        standings[team] = {
            "played": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "goals_for": 0,
            "goals_against": 0,
            "goal_difference": 0,
            "points": 0
        }

    return standings


def calculate_standings(teams, fixtures):
    """Calculate tournament standings from completed fixtures."""

    standings = initialize_standings(teams)

    for fixture in fixtures:

        # Ignore fixtures that have not been played.
        if fixture["status"] != "played":
            continue

        home = fixture["home_team"]
        away = fixture["away_team"]

        home_score = fixture["home_score"]
        away_score = fixture["away_score"]

        # Update matches played.
        standings[home]["played"] += 1
        standings[away]["played"] += 1

        # Update goals scored and conceded.
        standings[home]["goals_for"] += home_score
        standings[home]["goals_against"] += away_score

        standings[away]["goals_for"] += away_score
        standings[away]["goals_against"] += home_score

        # Determine the match outcome.
        if home_score > away_score:

            standings[home]["wins"] += 1
            standings[away]["losses"] += 1

            standings[home]["points"] += 3

        elif away_score > home_score:

            standings[away]["wins"] += 1
            standings[home]["losses"] += 1

            standings[away]["points"] += 3

        else:

            standings[home]["draws"] += 1
            standings[away]["draws"] += 1

            standings[home]["points"] += 1
            standings[away]["points"] += 1

    # Calculate goal difference.
    for team in standings:
        stats = standings[team]

        stats["goal_difference"] = (
            stats["goals_for"] - stats["goals_against"]
        )

    # Sort teams according to tournament ranking rules.
    sorted_standings = sorted(
        standings.items(),
        key=lambda item: (
            -item[1]["points"],
            -item[1]["goal_difference"],
            -item[1]["goals_for"],
            item[0].strip().casefold()
        )
    )

    return sorted_standings