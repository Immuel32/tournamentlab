from tournament.standings import calculate_standings


def determine_champion(teams, fixtures):
    """Determine the tournament champion after all fixtures are completed."""

    if not fixtures:
        return None

    # Check whether every fixture has been played.
    for fixture in fixtures:
        if fixture["status"] != "played":
            return None

    standings = calculate_standings(teams, fixtures)

    if not standings:
        return None

    # Check whether the top position is shared.
    top_team, top_stats = standings[0]

    if len(standings) > 1:
        second_stats = standings[1][1]

        ranking_keys = (
            "points",
            "goal_difference",
            "goals_for"
        )

        if all(top_stats[key] == second_stats[key] for key in ranking_keys):
            return None

    return top_team