from tournament.fixtures import FixtureManager

teams = ["red", "blue", "green", "yellow"]

manager = FixtureManager()

fixtures = manager.generate_fixtures(teams)

for fixture in fixtures:
    print(fixture)

print("Total fixtures:", len(fixtures))