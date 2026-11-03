import random

from tournament.results import record_result


def simulate_fixture(fixtures, fixture_id, seed):
    """Simulate one pending fixture using a reproducible random seed."""

    # A seed must be an integer, not a boolean.
    if isinstance(seed, bool) or not isinstance(seed, int):
        raise ValueError("Simulation seed must be an integer.")

    # A local random generator makes simulations reproducible.
    generator = random.Random(seed)

    # Generate a score between 0 and 5 for each team.
    home_score = generator.randint(0, 5)
    away_score = generator.randint(0, 5)

    # Reuse result recording to validate and save the result.
    return record_result(
        fixtures,
        fixture_id,
        home_score,
        away_score
    )