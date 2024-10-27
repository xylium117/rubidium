from tabulate import tabulate
import pandas as pd
from fuzzywuzzy import process
import numpy as np

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
1 - Premier League
2 - LaLiga 
3 - Bundesliga
4 - Seria A
5 - Ligue 1
6 - Liga Portugal
7 - Jupiler Pro League (Belgium)
8 - Major League Soccer
9 - 3F Superliga
10 - Eredvisie
11 - Liga Profesional
12 - EFL Championship
13 - Süper Lig
14 - Admiral Bundesliga (Austria)
15 - LaLiga 2
16 - Swiss Super League
17 - Ekstraklasa
18 - 2. Bundesliga
19 - Serie B
20 - K-League 1
21 - Allsvenskan
22 - Eliteserien
23 - Saudi Pro League
24 - Ligue 2
25 - cinch Premiership
26 - Chinese Super League
27 - Indian Super League
28 - Icons, Legends, Wonderkids
29 - Club Friendly
"""

df = pd.read_pickle("simulator/data/player_data2")
all_teams = [x for x in sorted([str(team) for team in df["club"].unique()[3:-1]]) if x != "nan"]

def get_league_input():
    try:
        num = int(input(leagues_message))
        assert num in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                       18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
        return num
    except (ValueError, AssertionError):
        print('Please enter a valid input!')
        get_league_input()

def teamInput(val, concat):
    while True:
        team = input(f"Enter Team {val} (type 'exit' to quit): ")
        if team.lower() == 'exit':
            exit()
        if team in concat:
            print(f"You selected: {team}")
            return team
        else:
            matches = process.extract(team, concat, limit=3)
            acc = [match for match, score in matches if score >= 70]
            if acc:
                if len(acc) > 1:
                    print("Did you mean one of the following clubs?")
                    for club in acc:
                        print(f"- {club}")
                else:
                    print(f"You selected: {acc[0]}")
                    return acc[0]
            else:
                print("Not in the list.")

def run():
    print(welcome_message)
    league_no = get_league_input()
    sel = []
    if league_no < 29:
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
        all_teams_leagues = []

        for club in all_teams:
            league = df.loc[df['club'] == club, 'league'].values[0]  # Get the league for the current club
            all_teams_leagues.append([club, league])
        _add = zip(["Icon", "Wonderkids", "Legends", "Hero"], ["Special", "Special", "Special", "Special"])
        concat = list(_add) + list(all_teams_leagues)
        _table = [list(tup) for tup in concat]
        data = [[i + 1] + sublist for i, sublist in enumerate(_table)]
        i = 0
        while i <= 700 - 30:
            print(
                tabulate(data[i : i + 15], headers=["", "Club", "League"], tablefmt="rounded_outline")
            )
            cmd = input("\nEnter 'n' for next page, 'p' for previous page, or 'q' to quit: ").strip().lower()
            if cmd == 'n' and i <= 700 - 30:
                i += 15
            elif cmd == 'p' and i >= 15:
                i -= 15
            elif cmd == 'q':
                break


        team_1 = teamInput(1, concat=["Icon", "Wonderkids", "Legends", "Hero"] + all_teams)
        team_2 = teamInput(2, concat=["Icon", "Wonderkids", "Legends", "Hero"] + all_teams)
        sel.append(team_1)
        sel.append(team_2)

        home_team = Team(sel[0])
        away_team = Team(sel[1])

        h = 0
        a = 0
        print("\n")
        print("LEG 1")
        print(sel[0].upper() + " VS " + sel[1].upper())
        match = Match(home_team, away_team, False, True)
        match.show_match_result()
        h += match.home_goals
        a += match.away_goals
        time.sleep(0.5)
        print("\n")
        print("LEG 2")
        print(sel[1].upper() + " VS " + sel[0].upper())
        match = Match(away_team, home_team, False, True)
        match.show_match_result()
        h += match.away_goals
        a += match.home_goals
        print("\nAGGREGATE SCORE:")
        print(f"{sel[0].upper()} {h} - {a} {sel[1].upper()}")
