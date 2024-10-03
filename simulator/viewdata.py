import pandas as pd
import configs.manager as cfgm
import configs.league as cfgl
from colorama import Fore, Back, Style
from tabulate import tabulate
from fuzzywuzzy import process

df_players_data = pd.read_pickle("data/player_data")

def view_Team():
    flag = True
    while flag:
        viewAll = input("\nEnter 'y' to view all clubs, or 'n' to skip: ")
        if viewAll == 'y':
            data = []
            n = 1
            for league_info in cfgl.leagues.values():
                for team in league_info["teams"]:
                    data.append([f"{Fore.BLUE}{n}.{Style.RESET_ALL}", f"{Fore.CYAN}{Style.BRIGHT}{team}{Style.RESET_ALL}"])
                    n += 1
            i = 0
            while i <= 90:
                print(
                    tabulate(data[i: i + 10], tablefmt="plain")
                )
                cmd = input("\nEnter 'n' for next page, 'p' for previous page, or 'q' to quit: ").strip().lower()
                if cmd == 'n' and i <= 90:
                    i += 10
                elif cmd == 'p' and i >= 10:
                    i -= 10
                elif cmd == 'q':
                    flag = False
                    break
        elif viewAll == 'n':
            break

    while True:
        clubname = input("\nEnter the name of a club: ")
        df_team_players_data = df_players_data[df_players_data["club"] == clubname]
        if not df_team_players_data.empty:
            print(clubname.upper())
            table_data = []

            for index, df_player in df_team_players_data.iterrows():
                ln = f"{Fore.YELLOW}{df_player['long_name']}{Style.RESET_ALL}"
                sn = f"{Fore.GREEN}{df_player['short_name']}{Style.RESET_ALL}"
                table_data.append([sn, ln])

            print(tabulate(table_data, tablefmt="plain"))
        else:
            print("Club name not found!")

def view_League():
    for country, league_info in cfgl.leagues.items():
        print(f"{Fore.RED}{Style.BRIGHT}{league_info['name'].upper()}:{Style.RESET_ALL}")
        for team in league_info["teams"]:
            print(f" - {Fore.YELLOW}{Style.BRIGHT}{team}{Style.RESET_ALL}")
        print()

def view_Players():
    print(f"{Fore.RED}{Style.BRIGHT}Premier League\nLaLiga\nBundesliga\nSerie A\nLigue 1\nCustom{Style.RESET_ALL}")

    leagues = ["Premier League", "LaLiga", "Bundesliga", "Serie A", "Ligue 1", "Custom"]
    league_name = ""
    while True:
        league_name = input("League (type 'exit' to quit): ")
        if league_name.lower() == 'exit':
            break
        if league_name in leagues:
            print(f"You selected: {league_name}")
            break
        else:
            matches = process.extract(league_name, leagues, limit=3)
            acc = [match for match, score in matches if score >= 60]
            if acc:
                if len(acc) > 1:
                    print("Did you mean one of the following leagues?")
                    for league in acc:
                        print(f"- {league}")
                else:
                    print(f"You selected: {acc[0]}")
                    break
            else:
                print("Not in the list.")
    country = ""
    if league_name == "LaLiga":
        country = "spain"
    elif league_name == "Premier League":
        country = "england"
    elif league_name == "Bundesliga":
        country = "germany"
    elif league_name == "Serie A":
        country = "italy"
    elif league_name == "Ligue 1":
        country = "france"
    elif league_name == "Custom":
        country = "special"
    league_info = cfgl.leagues[country]
    print(f"\n{Fore.RED}{Style.BRIGHT}{league_info['name']}:{Style.RESET_ALL}")
    league_data = []
    for team in league_info["teams"]:
        print(f"- {Fore.YELLOW}{Style.BRIGHT}{team}{Style.RESET_ALL}")
        league_data.append(team)

    team_name = ""
    while True:
        team_name = input("Club (type 'exit' to quit): ")
        if team_name.lower() == 'exit':
            break
        if team_name in league_data:
            print(f"You selected: {team_name}")
            break
        else:
            matches = process.extract(team_name, league_data, limit=3)
            acc = [match for match, score in matches if score >= 60]
            if acc:
                if len(acc) > 1:
                    print("Did you mean one of the following clubs?")
                    for club in acc:
                        print(f"- {club}")
                else:
                    print(f"You selected: {acc[0]}")
                    break
            else:
                print("Not in the list.")
    print()
    df_team_players_data = df_players_data[df_players_data["club"] == team_name]
    players = []
    if not df_team_players_data.empty:
        print(team_name.upper())
        table_data = []

        for index, df_player in df_team_players_data.iterrows():
            ln = f"{Fore.YELLOW}{df_player['long_name']}{Style.RESET_ALL}"
            sn = f"{Fore.GREEN}{df_player['short_name']}{Style.RESET_ALL}"
            players.append(df_player['short_name'])
            table_data.append([sn, ln])

        print(tabulate(table_data, tablefmt="plain"))
    print()
    player_name = ""
    while True:
        player_name = input("Player (type 'exit' to quit): ")
        if player_name.lower() == 'exit':
            break
        if player_name in players:
            print(f"You selected: {player_name}")
            break
        else:
            matches = process.extract(player_name, players, limit=3)
            acc = [match for match, score in matches if score >= 60]
            if acc:
                if len(acc) > 1:
                    print("Did you mean one of the following players?")
                    for player in acc:
                        print(f"- {player}")
                else:
                    print(f"You selected: {acc[0]}")
                    break
            else:
                print("Not in the list.")
    player_data = []
    df_player_data = df_team_players_data[df_team_players_data["short_name"] == player_name]
    for index, df_player in df_player_data.iterrows():
        ln = f"{Fore.YELLOW}{df_player['long_name']}{Style.RESET_ALL}"
        sn = f"{Fore.GREEN}{df_player['short_name']}{Style.RESET_ALL}"
        pos = f"{Fore.YELLOW}{df_player['player_positions']}{Style.RESET_ALL}"
        ovr = f"{Fore.BLUE}{df_player['overall']}{Style.RESET_ALL}"
        val = f"{Fore.MAGENTA}{df_player['value_eur']}{Style.RESET_ALL}"
        age = f"{Fore.RED}{df_player['age']}{Style.RESET_ALL}"
        dob = f"{Fore.WHITE}{df_player['dob']}{Style.RESET_ALL}"
        ht = f"{Fore.LIGHTYELLOW_EX}{df_player['height_cm']}{Style.RESET_ALL}"
        wt = f"{Fore.LIGHTMAGENTA_EX}{df_player['weight_kg']}{Style.RESET_ALL}"
        cl = f"{Fore.LIGHTCYAN_EX}{df_player['club']}{Style.RESET_ALL}"
        lg = f"{Fore.LIGHTGREEN_EX}{df_player['league']}{Style.RESET_ALL}"
        nat = f"{Fore.LIGHTWHITE_EX}{df_player['nationality']}{Style.RESET_ALL}"
        pac = f"{Fore.LIGHTBLUE_EX}{df_player['pace']}{Style.RESET_ALL}"
        shot = f"{Fore.LIGHTRED_EX}{df_player['shooting']}{Style.RESET_ALL}"
        pas = f"{Fore.LIGHTGREEN_EX}{df_player['passing']}{Style.RESET_ALL}"
        drib = f"{Fore.LIGHTYELLOW_EX}{df_player['dribbling']}{Style.RESET_ALL}"
        df = f"{Fore.LIGHTMAGENTA_EX}{df_player['defending']}{Style.RESET_ALL}"
        ph = f"{Fore.LIGHTCYAN_EX}{df_player['physic']}{Style.RESET_ALL}"
        gk_div = f"{Fore.LIGHTBLUE_EX}{df_player['gk_diving']}{Style.RESET_ALL}"
        gk_hand = f"{Fore.LIGHTGREEN_EX}{df_player['gk_handling']}{Style.RESET_ALL}"
        gk_kick = f"{Fore.LIGHTYELLOW_EX}{df_player['gk_kicking']}{Style.RESET_ALL}"
        gk_pos = f"{Fore.LIGHTMAGENTA_EX}{df_player['gk_positioning']}{Style.RESET_ALL}"
        gk_ref = f"{Fore.LIGHTCYAN_EX}{df_player['gk_reflexes']}{Style.RESET_ALL}"
        gk_spd = f"{Fore.LIGHTWHITE_EX}{df_player['gk_speed']}{Style.RESET_ALL}"
        player_data.append([sn, ln, pos, ovr, val, age, dob, ht, wt, cl, lg, nat, pac, shot, pas, drib, df, ph, gk_div, gk_hand, gk_kick, gk_pos, gk_ref, gk_spd])
    print(tabulate(player_data, headers=["Short Name", "Long Name", "Positions", "OVR", "Market Value", "Age", "Date of Birth", "Height", "Weight", "Club", "League", "Nationality", "Pace", "Shooting", "Passing", "Dribbling", "Defending", "Physical", "Diving", "Handling", "Kicking", "Positioning", "Reflexes", "Speed"], tablefmt="plain"))

cmd = input("\nEnter 'l' to view Leagues, 't' to view Teams, and 'p' to view Players: ")
if cmd == 't':
    view_Team()
elif cmd == 'l':
    view_League()
elif cmd == 'p':
    view_Players()
