class TeamManager:
    """Manage team registration and validation."""

    MIN_TEAMS = 4
    MAX_TEAMS = 8

    def __init__(self):
        # Store registered team names.
        self.teams = []

    def register_team(self, name):
        """Register one team after validating its name."""

        # Ensure the supplied name is a string.
        if not isinstance(name, str):
            raise ValueError("Team name must be a string.")

        # Remove unnecessary spaces around the name.
        name = name.strip()

        # Reject empty names.
        if not name:
            raise ValueError("Team name cannot be empty.")

        # Prevent duplicate names regardless of letter casing.
        for team in self.teams:
            if team.casefold() == name.casefold():
                raise ValueError("A team with this name already exists.")

        # Enforce the maximum number of teams.
        if len(self.teams) >= self.MAX_TEAMS:
            raise ValueError("A tournament cannot have more than 8 teams.")

        self.teams.append(name)

        return name

    def validate_team_count(self):
        """Check whether enough teams have been registered."""

        if len(self.teams) < self.MIN_TEAMS:
            raise ValueError("You need at least 4 teams to start.")

        return True

    def get_teams(self):
        """Return a copy of the registered teams."""
        return self.teams.copy()