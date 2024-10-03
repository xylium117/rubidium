from tabulate import tabulate

import time as time
from league import League
from team import Team
from match import Match
welcome_message = """
Welcome to the League Simulator!
You can use this project to simulate Football Leagues across the world
Please enter the league you would like to simulate:
"""

leagues_message = """
1 - LaLiga 
2 - Premier League
3 - Bundesliga
4 - Seria A
5 - Ligue 1
6 - Icons, Legends, Wonderkids
7 - Club Friendly
"""


def get_league_input():
    try:
        num = int(input(leagues_message))
        assert num in [1, 2, 3, 4, 5, 6, 7]
        return num
    except (ValueError, AssertionError):
        print('Please enter a valid input!')
        get_league_input()


def run():
    print(welcome_message)
    league_no = get_league_input()
    if league_no < 7:
        league = League(league_no)
        while True:
            user_input = input("Do you wish to see match events? (y/n): ").strip().lower()
            if user_input == 'y':
                print("You entered 'y'.")
                league.simulate_league(evt=True)
                break
            elif user_input == 'n':
                league.simulate_league(evt=False)
                break
    else:
        teams = (League(6).team_names + League(1).team_names + League(2).team_names + League(3).team_names
                 + League(4).team_names + League(5).team_names)
        sl = range(1, len(teams) + 1)
        table = zip(sl, teams)
        print(
            tabulate(table, headers=["", "Club"], tablefmt="rounded_outline")
        )
        selected_teams = []
        print("Enter 2 integers corresponding to team indices (1 to {}):".format(len(teams)))

        for i in range(2):
            while True:
                try:
                    index = int(input(f"Enter index for team {i + 1}: ")) - 1  # Adjusting for zero-based indexing
                    if 0 <= index < len(teams):
                        selected_teams.append(teams[index])
                        break  # Exit the loop if the input is valid
                    else:
                        print(f"Invalid index. Please enter a number between 1 and {len(teams)}.")
                except ValueError:
                    print("Invalid input. Please enter an integer.")

        home_team = Team(selected_teams[0])
        away_team = Team(selected_teams[1])

        h = 0
        a = 0
        print("\n")
        print("LEG 1")
        print(selected_teams[0].upper() + " VS " + selected_teams[1].upper())
        match = Match(home_team, away_team, False, True)
        match.show_match_result()
        h += match.home_goals
        a += match.away_goals
        time.sleep(0.5)
        print("\n")
        print("LEG 2")
        print(selected_teams[1].upper() + " VS " + selected_teams[0].upper())
        match = Match(away_team, home_team, False, True)
        match.show_match_result()
        h += match.away_goals
        a += match.home_goals
        print(f"{selected_teams[0].upper()} {h} - {a} {selected_teams[1].upper()}")
