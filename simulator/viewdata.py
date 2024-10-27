import pandas as pd
import configs.manager as cfgm
import configs.league as cfgl
from colorama import Fore, Back, Style
from tabulate import tabulate
from fuzzywuzzy import process

df_players_data = pd.read_pickle("data/player_data2")
all_teams = [x for x in sorted([str(team) for team in df_players_data["club"].unique()[3:-1]]) if x != "nan"]
concat = ["Icon", "Wonderkids", "Legends", "Hero"] + all_teams

def abbr(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B €"  # Billion
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.1f}M €"      # Million
    elif value >= 1_000:
        return f"{value / 1_000:.1f}k €"          # Thousand
    else:
        return f"{value:.2f} €"                   # Less than a thousand

def color(value):
    if value > 80:
        return f"{Fore.GREEN}{Style.BRIGHT}{value}{Style.RESET_ALL}"
    elif value > 70 and value <= 80:
        return f"{Fore.LIGHTGREEN_EX}{Style.BRIGHT}{value}{Style.RESET_ALL}"
    elif value > 50 and value <= 70:
        return f"{Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{value}{Style.RESET_ALL}"
    elif value <= 50:
        return f"{Fore.RED}{Style.BRIGHT}{value}{Style.RESET_ALL}"

def display_Data(player_name):
    df_player_data = df_players_data[df_players_data["short_name"] == player_name]
    player_data = []
    gk_data = []
    pos_data = []
    for index, df_player in df_player_data.iterrows():
        ln = f"{Fore.LIGHTYELLOW_EX}{df_player['long_name']}{Style.RESET_ALL}"
        sn = f"{Fore.LIGHTGREEN_EX}{df_player['short_name']}{Style.RESET_ALL}"
        pos = f"{Fore.LIGHTYELLOW_EX}{df_player['player_positions']}{Style.RESET_ALL}"
        ovr = color(df_player['overall'])
        val = f"{Fore.LIGHTMAGENTA_EX}{abbr(df_player['value_eur'])}{Style.RESET_ALL}"
        age = f"{Fore.LIGHTRED_EX}{df_player['age']}{Style.RESET_ALL}"
        dob = f"{Fore.LIGHTWHITE_EX}{df_player['dob']}{Style.RESET_ALL}"
        ht = f"{Fore.LIGHTYELLOW_EX}{df_player['height_cm']}{Style.RESET_ALL}"
        wt = f"{Fore.LIGHTMAGENTA_EX}{df_player['weight_kg']}{Style.RESET_ALL}"
        cl = f"{Fore.LIGHTCYAN_EX}{df_player['club']}{Style.RESET_ALL}"
        lg = f"{Fore.LIGHTGREEN_EX}{df_player['league']}{Style.RESET_ALL}"
        nat = f"{Fore.LIGHTWHITE_EX}{df_player['nationality']}{Style.RESET_ALL}"
        pac = color(df_player['pace'])
        shot = color(df_player['shooting'])
        pas = color(df_player['passing'])
        drib = color(df_player['dribbling'])
        df = color(df_player['defending'])
        ph = color(df_player['physic'])
        gk_div = color(df_player['gk_diving'])
        gk_hand = color(df_player['gk_handling'])
        gk_kick = color(df_player['gk_kicking'])
        gk_pos = color(df_player['gk_positioning'])
        gk_ref = color(df_player['gk_reflexes'])
        gk_spd = color(df_player['gk_speed'])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Short Name{Style.RESET_ALL}", sn])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Long Name{Style.RESET_ALL}", ln])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Player Positions{Style.RESET_ALL}", pos])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Market Value{Style.RESET_ALL}", val])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Age{Style.RESET_ALL}", age])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}DOB{Style.RESET_ALL}", dob])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Height (in cm){Style.RESET_ALL}", ht])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Weight (in kg){Style.RESET_ALL}", wt])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Club{Style.RESET_ALL}", cl])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}League{Style.RESET_ALL}", lg])
        player_data.append([f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}Nationality{Style.RESET_ALL}", nat])
        if "GK" in pos:
            gk_data.append([ovr, gk_div, gk_hand, gk_kick, gk_pos, gk_ref, gk_spd])
        else:
            pos_data.append([ovr, pac, shot, pas, drib, df, ph])
        print(tabulate(player_data,
                   tablefmt="plain", numalign="center"))
        if "GK" in pos:
            print(tabulate(gk_data,
                       headers=[f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}OVR{Style.RESET_ALL}", "DIV", "HAN", "KIC", "POS",
                                "REF", "SPE"],
                       tablefmt="rounded_grid", numalign="center"))
        else:
            print(tabulate(pos_data,
                       headers=[f"{Fore.LIGHTWHITE_EX}{Style.BRIGHT}OVR{Style.RESET_ALL}", "PAC", "SHO", "PAS", "DRI",
                                "DEF", "PHY"], tablefmt="rounded_grid", numalign="center"))


def view_Team():
    flag = True
    while flag:
        viewAll = input("\nEnter 'y' to view all clubs, or 'n' to skip: ")
        if viewAll == 'y':
            data = []
            n = 1
            for team in concat:
                data.append([f"{Fore.LIGHTBLUE_EX}{n}.{Style.RESET_ALL}", f"{Fore.LIGHTCYAN_EX}{Style.BRIGHT}{team}{Style.RESET_ALL}"])
                n += 1
            i = 0
            while i <= 670:
                print(
                    tabulate(data[i: i + 15], tablefmt="plain")
                )
                cmd = input("\nEnter 'n' for next page, 'p' for previous page, or 'q' to quit: ").strip().lower()
                if cmd == 'n' and i <= 670:
                    i += 15
                elif cmd == 'p' and i >= 15:
                    i -= 15
                elif cmd == 'q':
                    flag = False
                    break
        elif viewAll == 'n':
            break

    while True:
        clubname = ""
        while True:
            clubname = input("\nEnter the name of a club (type 'exit' to quit): ")
            if clubname.lower() == 'exit':
                exit()
            if clubname in concat:
                print(f"You selected: {clubname}")
                clubname = clubname
                break
            else:
                matches = process.extract(clubname, concat, limit=5)
                acc = [match for match, score in matches if score >= 70]
                if acc:
                    if len(acc) > 1:
                        print("Did you mean one of the following clubs?")
                        for club in acc:
                            print(f"- {club}")
                    else:
                        print(f"You selected: {acc[0]}")
                        clubname = acc[0]
                        break
                else:
                    print("Not in the list.")
        df_team_players_data = df_players_data[df_players_data["club"] == clubname]
        if not df_team_players_data.empty:
            print(clubname.upper())
            table_data = []

            for index, df_player in df_team_players_data.iterrows():
                ln = f"{Fore.LIGHTYELLOW_EX}{df_player['long_name']}{Style.RESET_ALL}"
                sn = f"{Fore.LIGHTGREEN_EX}{df_player['short_name']}{Style.RESET_ALL}"
                table_data.append([sn, ln])

            print(tabulate(table_data, tablefmt="plain"))
        elif clubname.strip().lower() == 'exit':
            exit()
        else:
            print("Club name not found!")

def view_League():
    for country, league_info in cfgl.leagues.items():
        print(f"{Fore.LIGHTRED_EX}{Style.BRIGHT}{league_info['name'].upper()}:{Style.RESET_ALL}")
        for team in league_info["teams"]:
            print(f" - {Fore.LIGHTYELLOW_EX}{Style.BRIGHT}{team}{Style.RESET_ALL}")
        print()

def view_Players():
    all_players = df_players_data["short_name"].tolist()
    all_teams = [x for x in sorted([str(team) for team in df_players_data["club"].unique()[3:-1]]) if x != "nan"]
    concat = ["Icon", "Wonderkids", "Legends", "Hero"] + all_teams
    while True:
        inp = input("\nSearch by Player Name? (y/n): ").strip().lower()
        if inp == "y":
            player_name = ""
            while True:
                player_name = input("Player name (type 'exit' to quit): ")
                if player_name.lower() == 'exit':
                    break
                if player_name in all_players:
                    print(f"You selected: {player_name}")
                    break
                else:
                    matches = process.extract(player_name, all_players, limit=3)
                    acc = [match for match, score in matches if score >= 60]
                    if acc:
                        if len(acc) > 1:
                            print("Did you mean one of the following players?")
                            for p in acc:
                                print(f"- {p}")
                        else:
                            print(f"You selected: {acc[0]}")
                            player_name = acc[0]
                            break
                    else:
                        print("Not in the list.")
            display_Data(player_name)
        elif inp == "n":
            team_name = ""
            while True:
                team_name = input("Club (type 'exit' to quit): ")
                if team_name.lower() == 'exit':
                    exit()
                if team_name in concat:
                    print(f"You selected: {team_name}")
                    team_name = team_name
                    break
                else:
                    matches = process.extract(team_name, concat, limit=5)
                    acc = [match for match, score in matches if score >= 70]
                    if acc:
                        if len(acc) > 1:
                            print("Did you mean one of the following clubs?")
                            for club in acc:
                                print(f"- {club}")
                        else:
                            print(f"You selected: {acc[0]}")
                            team_name = acc[0]
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
                    ln = f"{Fore.LIGHTYELLOW_EX}{df_player['long_name']}{Style.RESET_ALL}"
                    sn = f"{Fore.LIGHTGREEN_EX}{df_player['short_name']}{Style.RESET_ALL}"
                    players.append(df_player['short_name'])
                    table_data.append([sn, ln])

                print(tabulate(table_data, tablefmt="plain"))
            print()
            player_name = ""
            while True:
                player_name = input("Player (type 'exit' to quit): ")
                if player_name.lower() == 'exit':
                    exit()
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
                            player_name = f"{acc[0]}"
                            break
                    else:
                        print("Not in the list.")
                print(player_name)
            display_Data(player_name)



cmd = input("\nEnter 'l' to view Leagues, 't' to view Teams, and 'p' to view Players: ")
if cmd == 't':
    view_Team()
elif cmd == 'l':
    view_League()
elif cmd == 'p':
    view_Players()
