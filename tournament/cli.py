from tournament.teams import TeamManager
from tournament.fixtures import FixtureManager
from tournament.results import record_result
from tournament.standings import calculate_standings
from tournament.champion import determine_champion
from tournament.storage import StorageManager
from tournament.simulation import simulate_fixture


class TournamentCLI:
    """Connect tournament features through a command-line interface."""

    def __init__(self):
        self.team_manager = TeamManager()
        self.fixture_manager = FixtureManager()
        self.storage = StorageManager()

        self.fixtures = []

        # Restore previously saved tournament data.
        self.load_tournament()

    def load_tournament(self):
        """Load saved teams and fixtures when the application starts."""

        try:
            data = self.storage.load()

            # Restore registered teams.
            self.team_manager.teams = data["teams"]

            # Restore tournament fixtures.
            self.fixtures = data["fixtures"]

        except ValueError as error:
            print(f"\nCould not load tournament: {error}")

    def save_tournament(self):
        """Save the current tournament."""

        self.storage.save(
            self.team_manager.teams,
            self.fixtures
        )

    def register_teams(self):
        """Register the number of teams selected for a new tournament."""

        if self.team_manager.teams:
            print("\nTeams are already registered.")
            print("Start a new tournament before registering new teams.")
            return

        print("\n--- Register Teams ---")

        try:
            team_count = int(input("How many teams? (4-8): "))

            if not TeamManager.MIN_TEAMS <= team_count <= TeamManager.MAX_TEAMS:
                print("Please select between 4 and 8 teams.")
                return

            # Register exactly the number of teams selected.
            for number in range(team_count):
                while True:
                    name = input(f"Enter team {number + 1} name: ")

                    try:
                        self.team_manager.register_team(name)
                        print(f"{name.strip()} registered successfully.")
                        break

                    except ValueError as error:
                        print(f"Error: {error}")

            self.save_tournament()
            print("\nTeam registration completed successfully.")

        except ValueError:
            print("Please enter a valid number.")
        
    def generate_fixtures(self):
        """Generate the single round-robin schedule."""

        if self.fixtures:
            print("\nFixtures have already been generated.")
            return

        try:
            self.team_manager.validate_team_count()

            self.fixtures = self.fixture_manager.generate_fixtures(
                self.team_manager.get_teams()
            )

            self.save_tournament()

            print(
                f"\nSuccessfully generated "
                f"{len(self.fixtures)} fixtures."
            )

        except ValueError as error:
            print(f"\nError: {error}")

    def list_fixtures(self):
        """Display all scheduled fixtures."""

        print("\n--- Tournament Fixtures ---")

        if not self.fixtures:
            print("No fixtures have been generated yet.")
            return

        for fixture in self.fixtures:

            if fixture["status"] == "played":
                result = (
                    f'{fixture["home_score"]} - '
                    f'{fixture["away_score"]}'
                )
            else:
                result = "Pending"

            print(
                f'ID: {fixture["id"]} | '
                f'{fixture["home_team"]} vs '
                f'{fixture["away_team"]} | '
                f'{result}'
            )

    def enter_result(self):
        """Allow the user to record a match result."""

        print("\n--- Record Match Result ---")

        try:
            fixture_id = int(input("Enter fixture ID: "))
            home_score = int(input("Enter home team score: "))
            away_score = int(input("Enter away team score: "))

            record_result(
                self.fixtures,
                fixture_id,
                home_score,
                away_score
            )

            self.save_tournament()

            print("\nMatch result recorded successfully.")

        except ValueError as error:
            print(f"\nError: {error}")

    def show_standings(self):
        """Display the calculated tournament standings."""

        print("\n--- Tournament Standings ---")

        if not self.team_manager.teams:
            print("No teams have been registered.")
            return

        standings = calculate_standings(
            self.team_manager.teams,
            self.fixtures
        )

        print(
            f"\n{'Team':<15}"
            f"{'P':<5}"
            f"{'W':<5}"
            f"{'D':<5}"
            f"{'L':<5}"
            f"{'GF':<5}"
            f"{'GA':<5}"
            f"{'GD':<5}"
            f"{'Pts':<5}"
        )

        for team, stats in standings:
            print(
                f"{team:<15}"
                f"{stats['played']:<5}"
                f"{stats['wins']:<5}"
                f"{stats['draws']:<5}"
                f"{stats['losses']:<5}"
                f"{stats['goals_for']:<5}"
                f"{stats['goals_against']:<5}"
                f"{stats['goal_difference']:<5}"
                f"{stats['points']:<5}"
            )

    def simulate_match(self):
        """Explicitly simulate one pending fixture."""

        print("\n--- Simulate Match ---")

        try:
            fixture_id = int(input("Enter fixture ID: "))
            seed = int(input("Enter simulation seed: "))

            fixture = simulate_fixture(
                self.fixtures,
                fixture_id,
                seed
            )

            self.save_tournament()

            print(
                f"\nSimulation result: "
                f'{fixture["home_team"]} '
                f'{fixture["home_score"]} - '
                f'{fixture["away_score"]} '
                f'{fixture["away_team"]}'
            )

        except ValueError as error:
            print(f"\nError: {error}")

    def show_champion(self):
        """Display the champion when the tournament is complete."""

        print("\n--- Tournament Champion ---")

        if not self.fixtures:
            print("No tournament fixtures exist yet.")
            return

        champion = determine_champion(
            self.team_manager.teams,
            self.fixtures
        )

        if champion is None:

            pending = any(
                fixture["status"] != "played"
                for fixture in self.fixtures
            )

            if pending:
                print("Tournament still in progress.")
            else:
                print("The tournament has ended in a tie.")

        else:
            print(f"Champion: {champion}")

    def show_menu(self):
        """Display the main application menu."""

        print("\n================================")
        print("       TOURNAMENTLAB")
        print("    ESPORTS LEAGUE MANAGER")
        print("================================")

        print("1. Register teams")
        print("2. Generate fixtures")
        print("3. List fixtures")
        print("4. Record match result")
        print("5. View standings")
        print("6. Simulate a match")
        print("7. Show champion")
        print("8. Save tournament")
        print("9. Exit")

    def run(self):
        """Run the main application loop."""

        print("\nWelcome to TournamentLab!")

        while True:

            self.show_menu()

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                if self.fixtures:
                    print(
                        "\nRegistration is closed because "
                        "fixtures have already been generated."
                    )
                else:
                    self.register_teams()

            elif choice == "2":
                self.generate_fixtures()

            elif choice == "3":
                self.list_fixtures()

            elif choice == "4":
                self.enter_result()

            elif choice == "5":
                self.show_standings()

            elif choice == "6":
                self.simulate_match()

            elif choice == "7":
                self.show_champion()

            elif choice == "8":
                self.save_tournament()
                print("\nTournament saved successfully.")

            elif choice == "9":
                self.save_tournament()
                print("\nTournament saved. Goodbye!")
                break

            else:
                print("\nInvalid option. Please select 1–9.")