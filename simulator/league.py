import pandas as pd
import numpy as np
from tabulate import tabulate
import asciichartpy as acp
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

import configs.league as scl
from match import Match
from team import Team
import random as random


class League:
    LEAGUE_TABLE_ATTRIBUTES = [
        "Club",
        "Matches Played",
        "Wins",
        "Draws",
        "Losses",
        "Points",
        "GF",
        "GA",
        "GD",
    ]

    auto = True
    auto2 = True
    def __init__(self, option):
        self.week = 0
        self.name = scl.leagues[scl.countries[option]]["name"]
        self.players = {}
        self.teams = {}
        self.team_names = scl.leagues[scl.countries[option]]["teams"]
        self.set_teams()
        self.set_players()
        self.schedule = self.create_balanced_round_robin(self.team_names)
        self.standings = self.init_league_table()

    def set_teams(self):
        for name in self.team_names:
            team = Team(name)
            self.teams[name] = team

    def set_players(self):
        for team in self.teams.values():
            self.players.update(team.players)

    def create_balanced_round_robin(self, teams):
        """Create a schedule for the teams in the list and return it"""
        schedule = []
        if len(teams) % 2 == 1:
            teams = teams + [None]

        team_count = len(teams)
        mid = team_count // 2

        for _ in range(team_count - 1):
            first_half = teams[:mid]
            second_half = teams[mid:]
            second_half.reverse()

            round_schedule = [(t1, t2) for t1, t2 in zip(first_half, second_half)]
            round_schedule += [(t2, t1) for t1, t2 in zip(second_half, first_half)]

            schedule.append(round_schedule)

            teams.insert(1, teams.pop())  # Rotate the list
        return schedule

    def init_league_table(self):
        table = pd.DataFrame(columns=League.LEAGUE_TABLE_ATTRIBUTES)
        table.index = np.arange(1, len(table)+1)
        for team in self.team_names:
            row = pd.DataFrame(
                [[team, 0, 0, 0, 0, 0, 0, 0, 0]],
                columns=League.LEAGUE_TABLE_ATTRIBUTES,
            )
            table = pd.concat([table, row])
        table = table.reset_index(drop=True)
        table.index = table.index + 1
        table.index = np.arange(1, len(table) + 1)
        return table

    def show_league_table(self):
        table = self.standings
        table.index = np.arange(1, len(table) + 1)
        print(
            tabulate(self.standings, headers=self.standings.columns, tablefmt="rounded_outline")
        )

    def update_league_table(self, match):
        (result, winner, loser) = match.evaluate_match_result()
        table = self.standings
        num_winner_goals = match.stats[winner]["Goal"]
        num_loser_goals = match.stats[loser]["Goal"]
        goal_difference = num_winner_goals - num_loser_goals
        if result == "Draw":
            for team in [winner, loser]:
                table.loc[(table["Club"] == team.name)] += [
                    "",
                    1,
                    0,
                    1,
                    0,
                    1,
                    num_winner_goals,
                    num_loser_goals,
                    0,
                ]
        else:
            table.loc[(table["Club"] == winner.name)] += [
                "",
                1,
                1,
                0,
                0,
                3,
                num_winner_goals,
                num_loser_goals,
                goal_difference,
            ]
            table.loc[(table["Club"] == loser.name)] += [
                "",
                1,
                0,
                0,
                1,
                0,
                num_loser_goals,
                num_winner_goals,
                -goal_difference,
            ]
        table.sort_values(by="Points", inplace=True, ascending=False)
        table.reset_index(drop=True, inplace=True)

    def simulate_match(self, home_team_name, away_team_name, evt):
        home_team = self.teams[home_team_name]
        away_team = self.teams[away_team_name]
        print("\n")
        print(home_team_name.upper() + " VS " + away_team_name.upper())
        match = Match(home_team, away_team, self.auto, evt)
        match.show_match_result()
        print("\n")
        self.update_league_table(match)

    def simulate_week(self, evt):
        for home_team, away_team in self.schedule[self.week]:
            self.simulate_match(home_team, away_team, evt)
            while self.auto:
                user_input = input("Enter 'y' to continue simulating matchdays, 'n' to stop, and 'a' to auto: ").strip().lower()
                if user_input == 'y':
                    print("You entered 'y'.")
                    break
                elif user_input == 'n':
                    exit()
                elif user_input == 'a':
                    self.auto = False
        self.week += 1

    def simulate_league(self, evt):
        while self.week < len(self.schedule):
            self.simulate_week(evt)
            self.show_league_table()
            while self.auto2:
                user_input = input("Enter 'y' to continue simulating matchweeks, 'n' to stop, and 'a' to auto: ").strip().lower()
                if user_input == 'y':
                    print("You entered 'y'.")
                    break
                elif user_input == 'n':
                    exit()
                elif user_input == 'a':
                    self.auto2 = False
        players = list(self.players.values())
        while True:
            user_input = input("Do you wish to see player statistics? (y/n): ").strip().lower()
            if user_input == 'y':
                print("You entered 'y'.")
                break
            elif user_input == 'n':
                exit()

        name = []
        pos = []
        club = []
        goals = []
        assists = []
        saves = []
        yellow = []
        red = []
        motm = []
        motms = []
        for player in players:
            name.append(player.name)
            pos.append(player.pos2)
            club.append(player.club)
            goals.append(player.goals)
            assists.append(round(player.keypasses/8.0))
            saves.append(round(player.saves/2.0))
            yellow.append(round(player.yellow/2.0))
            red.append(player.red)
            motms.append(player.motmscore)
            motm.append(min((player.pots/100.0) + 2, 9.9 - random.choice([0.3, 0.3, 0.2, 0.2, 0.1, 0.2, 0.1, 0.2, 0.3, random.randint(3, 6)/10.0, random.randint(3, 6)/10.0, random.randint(3, 6)/10.0, random.randint(3, 6)/10.0, random.randint(3, 6)/10.0, random.randint(3, 6)/10.0])))
        keys = ["Player", "Position", "Club", "Goals", "Assists", "Saves", "Yellow Cards", "Red Cards", "MOTM Awards", "Rating"]
        dict = {
            "Player" : name,
            "Position" : pos,
            "Club" : club,
            "Goals" : goals,
            "Assists" : assists,
            "Saves" : saves,
            "Yellow Cards" : yellow,
            "Red Cards" : red,
            "MOTM Awards" : motms,
            "Rating" : motm,
        }

        df = pd.DataFrame(dict)
        df_sorted = df.sort_values(by='Rating', ascending=False)
        df_sorted.reset_index(drop=True, inplace=True)
        print(tabulate(df_sorted.head(15), tablefmt="rounded_outline", stralign="center", numalign="center", showindex=False, headers=["Player", "Position", "Club", "Goals", "Assists", "Saves", "Yellow Cards", "Red Cards", "MOTM Awards", "Rating"]))

        print("See individual stats of players (enter 0 to exit): ")
        while True:
            inp = 0
            while True:
                inp = int(input("Enter an integer between 1 and 15: "))
                if inp >= 1 and inp <= 15:
                    break
                elif inp == 0:
                    exit()
            print()
            dict = df_sorted.to_dict()
            player_keys = list(dict['Player'].keys())
            player_key = player_keys[inp - 1]
            name = dict['Player'][player_key]
            for player in players:
                if player.name == name:
                    print("Showing SEASON STATS of ", name.upper())
                    if player.pos2 == "goalkeeper":
                        print("Saves per Match:")
                        print(acp.plot(player.ssnsaves, {"height" : 10, "colors" : [acp.yellow]}))
                        while True:
                            exp = input("Export graph? (y/n): ")
                            if exp == 'y':
                                font1 = {'family': 'serif', 'color': 'darkred', 'size': 20}
                                font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}

                                plt.figure(name)
                                plt.title("Saves per Match", fontdict=font1, loc='left')

                                plt.xlabel("Matchdays", fontdict=font2)
                                plt.ylabel("Saves", fontdict=font2)
                                x = np.array([x for x in range(len(player.ssnsaves))])
                                y = np.array(player.ssnsaves)

                                X_Y_Spline = interp1d(x, y, kind="cubic")
                                X_ = np.linspace(x.min(), x.max(), 500)
                                Y_ = X_Y_Spline(X_)
                                plt.plot(X_, Y_, color = "yellow")
                                plt.show()
                                plt.close()
                                break
                            elif exp == 'n':
                                break
                    else:
                        print("Goals per Match:")
                        print(acp.plot(player.ssngoals, {"height" : 10, "colors" : [acp.green]}))
                        print("Assists per Match:")
                        print(acp.plot(player.ssnpasses, {"height" : 10, "colors" : [acp.blue]}))
                        while True:
                            exp = input("Export graphs? (y/n): ")
                            if exp == 'y':
                                font1 = {'family': 'serif', 'color': 'darkred', 'size': 15}
                                font2 = {'family': 'serif', 'color': 'darkred', 'size': 10}
                                plt.figure(name + " (GOALS)")
                                x = np.array([x for x in range(len(player.ssngoals))])
                                y = np.array(player.ssngoals)

                                X_Y_Spline = interp1d(x, y, kind="cubic")
                                X_ = np.linspace(x.min(), x.max(), 500)
                                Y_ = X_Y_Spline(X_)
                                plt.plot(X_, Y_, color="green")
                                plt.title("Goals per Match", fontdict=font1, loc='left')
                                plt.xlabel("Matchdays", fontdict=font2)
                                plt.ylabel("Goals", fontdict=font2)
                                plt.show()
                                plt.close()

                                plt.figure(name + " (ASSISTS)")
                                x = np.array([x for x in range(len(player.ssnpasses))])
                                y = np.array(player.ssnpasses)

                                X_Y_Spline = interp1d(x, y, kind="cubic")
                                X_ = np.linspace(x.min(), x.max(), 500)
                                Y_ = X_Y_Spline(X_)
                                plt.plot(X_, Y_, color="blue")
                                plt.title("Assists per Match", fontdict=font1, loc='left')
                                plt.xlabel("Matchdays", fontdict=font2)
                                plt.ylabel("Assists", fontdict=font2)
                                plt.show()
                                plt.close()
                                break
                            elif exp == 'n':
                                break
