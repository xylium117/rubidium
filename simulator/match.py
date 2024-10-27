import copy
import random
from tabulate import tabulate

from configs.odds import odds
from event import Event


class Match:
    reverse = {"Home": "Away", "Away": "Home"}
    eventkeys = list(odds[0]["Home"]["Events"].keys())
    foulkeys = ["Free kick won", "Yellow card", "Second yellow card", "Red card"]
    auto = True # Control output for unit test
    evt = True # Control output for unit test
    redcard = [] # card tally
    yellowcard = [] # card tally

    def __init__(self, home_side, away_side, auto, evt):
        self.odds = copy.deepcopy(odds)
        tlist = copy.deepcopy(Match.eventkeys)
        tlist.extend(
            ["On target", "Saved", "Off target", "Blocked", "Hit the bar", "Goal"]
        )
        self.home_stats = dict(zip(tlist, [0] * len(tlist)))
        self.away_stats = dict(zip(tlist, [0] * len(tlist)))
        self.home_side = home_side
        self.away_side = away_side
        self.sides = {home_side: "Home", away_side: "Away"}
        self.reverse = {home_side: away_side, away_side: home_side}
        self.matchevents = []
        self.stats = dict(
            zip(
                [self.home_side, self.away_side],
                [copy.copy(self.home_stats), copy.copy(self.away_stats)],
            )
        )
        self.home_players = home_side.players
        self.home_squad = home_side.squad
        self.away_players = away_side.players
        self.away_squad = away_side.squad
        self.set_odds()
        self.set_events(home_side, away_side)
        self.auto = auto
        self.redcard.clear()
        self.yellowcard.clear()
        self.evt = evt
        self.hscore = 0
        self.ascore = 0

    def bar(self, a, b):
        total = a + b
        if a == 0 and b == 0:
            total = 50
            a = 25
        if total == 0:  # Prevent division by zero
            al = 0
            bl = 50
        else:
            al = int(50 * (a / total))
            bl = 50 - al
        return f"[{'█' * al}{'░' * bl}]"

    def set_odds(self):
        hdf = (self.home_side.defence ** 2 * self.home_side.midfield) / (
                self.away_side.attack ** 2 * self.away_side.midfield
        )
        adf = (self.away_side.defence ** 2 * self.away_side.midfield) / (
                self.home_side.attack ** 2 * self.home_side.midfield
        )
        for minute in range(100):
            self.odds[minute]["Home"]["Events"]["Attempt"] = self.odds[minute]["Home"][
                                                                 "Events"
                                                             ]["Attempt"] / (adf ** 2.33)
            self.odds[minute]["Away"]["Events"]["Attempt"] = self.odds[minute]["Away"][
                                                                 "Events"
                                                             ]["Attempt"] / (hdf ** 2.33)

    def add_event(self, event):
        for e in event.evaluate_event():
            if e.player.name not in self.redcard:
                if e.event == "Substitution":
                    if self.stats[e.side][e.event] < 3:
                        self.track_event(e)
                elif e.event == "Red card" or e.event == "Sending off" or e.event == "Second yellow card":
                    self.redcard.append(e.player.name)
                    self.yellowcard.clear()
                elif e.event == "Yellow card" and e.player.name not in self.yellowcard:
                    self.yellowcard.append(e.player.name)
                elif e.event == "Yellow card" and e.player.name in self.yellowcard:
                    e.event = "Second yellow card"
                    print("########################################################################")
                    self.redcard.append(e.player.name)
                else:
                    self.track_event(e)

                e.show_event(self.auto, evt=self.evt)
                self.matchevents.append(e)

    def set_events(self, home_side, away_side):
        for minute in range(100):
            for _ in range(135):
                if random.uniform(0, 1) < self.odds[minute]["Event"]:
                    plist = []
                    plist.append(self.odds[minute]["Home"]["Probability"])
                    plist.append(self.odds[minute]["Away"]["Probability"])
                    side = random.choices([self.home_side, self.away_side], plist, k=1)[0]
                    event = random.choices(
                        Match.eventkeys,
                        list(self.odds[minute][self.sides[side]]["Events"].values()),
                        k=1
                    )[0]
                    if event not in Match.foulkeys:
                        e = Event(event, side, minute)
                        e.set_home_and_away_sides(home_side, away_side)
                        self.add_event(e)

    def track_event(self, event):
        if event.side == self.home_side:
            self.home_stats[event.event] = self.home_stats[event.event] + 1
        else:
            self.away_stats[event.event] = self.away_stats[event.event] + 1
        self.stats = dict(
            zip(
                [self.home_side, self.away_side],
                [copy.copy(self.home_stats), copy.copy(self.away_stats)],
            )
        )

    def evaluate_match_result(self):
        hg = self.stats[self.home_side]["Goal"]
        ag = self.stats[self.away_side]["Goal"]
        if hg == ag:
            return ("Draw", self.home_side, self.away_side)
        elif hg > ag:
            return ("Win", self.home_side, self.away_side)
        else:
            return ("Win", self.away_side, self.home_side)

    def show_match_result(self):
        onTargetA = 0
        onTargetB = 0
        shotA = 0
        shotB = 0
        posA = self.home_side.midfield ** 0.2 * self.home_side.attack
        posB = self.away_side.midfield ** 0.2 * self.away_side.attack
        savesA = 0
        savesB = 0
        yellowA = 0
        yellowB = 0
        redA = 0
        redB = 0
        offsideA = 0
        offsideB = 0
        cornerA = 0
        cornerB = 0
        self.home_goals = self.stats[self.home_side]["Goal"]
        self.away_goals = self.stats[self.away_side]["Goal"]
        if self.home_goals > self.away_goals:
            print(f"{self.home_side.name} won the match")
            print(f"Score {self.home_goals} - {self.away_goals}")
        elif self.away_goals > self.home_goals:
            print(f"{self.away_side.name} won the match")
            print(f"Score {self.home_goals} - {self.away_goals}")
        else:
            print(
                f"The match between {self.home_side.name} and {self.away_side.name} was a Draw"
            )
            print(f"Score {self.home_goals} - {self.away_goals}")



        # Prepare data for the events table
        event_data = []
        for event in self.matchevents:
            timestamp = f"{event.minute}'"  # Center-align the timestamp
            if event.side == self.home_side:  # Player A is right aligned
                if event.event == "Goal":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                    onTargetA += 1
                elif event.event == "Own goal":
                    event_data.append(["", timestamp, event.player.name + " (O.G.)"])
                    self.away_goals += 1
                elif event.event == "Saved":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                    onTargetB += 1
                    savesB += 1
                elif event.event == "Yellow card":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                    yellowA += 1
                elif event.event == "Red card" or event.event == "Sending off" or event.event == "Second yellow card":
                    event_data.append([event.player.name + " (RED CARD)", timestamp, ""])
                    redA += 1
                elif event.event == "Offside":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                    offsideA += 1
                elif event.event == "Corner":
                    cornerA += 1
                elif event.event == "On Target":
                    onTargetA += 1
                elif event.event == "Blocked":
                    onTargetA += 1
                elif event.event == "Attempt":
                    shotA += 1
                elif event.event == "Key Pass" or event.event == "Free kick won" or event.event == "Corner":
                    posA += 35 + random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
            elif event.side == self.away_side:  # Player B is left aligned
                if event.event == "Goal":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    onTargetB += 1
                elif event.event == "Own goal":
                    event_data.append([event.player.name + " (O.G)", timestamp, ""])
                    self.home_goals += 1
                elif event.event == "Corner":
                    cornerB += 1
                elif event.event == "Saved":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    onTargetA += 1
                    savesA += 1
                elif event.event == "Yellow card":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    yellowB += 1
                elif event.event == "Red card" or event.event == "Sending off" or event.event == "Second yellow card":
                    event_data.append(["", timestamp, event.player.name + " (RED CARD) "])
                    redB += 1
                elif event.event == "Offside":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    offsideB += 1
                elif event.event == "On Target":
                    onTargetB += 1
                elif event.event == "Attempt":
                    shotB += 1
                elif event.event == "Blocked":
                    onTargetB += 1
                elif event.event == "Key Pass" or event.event == "Free kick won" or event.event == "Corner":
                    posB += 35

        pA = (int)((posA * 100)/(posA + posB))
        pB = 100 - pA
        # Print the events without headers
        print(tabulate(event_data, tablefmt="rounded_outline", stralign="center", numalign="center", showindex=False,
                       headers=[self.home_side.name.upper(), f"{self.home_goals}  -  {self.away_goals}", self.away_side.name.upper()]))
        self.hscore = self.home_goals
        self.ascore = self.away_goals
        # display stats
        stats = [
            ["Possession", f"{pA}", self.bar(pA, pB), f"{pB}"],
            ["Attempts (On Target)", f"{shotA}({onTargetA})", self.bar(shotA + onTargetA, shotB + onTargetB), f"{shotB}({onTargetB})"],
            ["Saves", f"{savesA}", self.bar(savesA, savesB), f"{savesB}"],
            ["Offsides", f"{offsideA}", self.bar(offsideA, offsideB), f"{offsideB}"],
            ["Corners", f"{cornerA}", self.bar(cornerA, cornerB), f"{cornerB}"],
            ["Yellow Cards/Red Cards", f"{yellowA}/{redA}", self.bar(yellowA + redA, yellowB + redB), f"{yellowB}/{redB}"],
        ]

        # Print the stats section
        print(tabulate(stats, tablefmt="plain", numalign="center", stralign="center", showindex=False, headers=["", self.home_side.name.upper(), f"{self.home_goals}  -  {self.away_goals}", self.away_side.name.upper()]))
        # MOTM logic
        home_players = list(self.home_players.values())
        away_players = list(self.away_players.values())
        motmH = home_players[0]
        for player in home_players:
            if player.motm > motmH.motm:
                motmH = player

        motmA = away_players[0]
        for player in away_players:
            if player.motm > motmA.motm:
                motmA = player

        s = ""
        if self.home_goals > self.away_goals:
            if motmA.motm >= 2 * motmH.motm:
                s = motmA.name
                motmA.motmscore += 1
            else:
                s = motmH.name
                motmH.motmscore += 1
        elif self.home_goals < self.away_goals:
            if motmH.motm >= 2 * motmA.motm:
                s = motmH.name
                motmH.motmscore += 1
            else:
                s = motmA.name
                motmA.motmscore += 1
        elif self.home_goals == self.away_goals:
            if motmH.motm > motmA.motm:
                s = motmH.name
                motmH.motmscore += 1
            else:
                s = motmA.name
                motmA.motmscore += 1

        print("Man of the Match:", s)

        # store in season data
        for player in home_players:
            player.motm = 0
            player.ssnsaves.append(round(player.matchsaves / 2.0))
            player.ssngoals.append(player.matchgoals)
            player.ssnpasses.append(round(player.matchpasses / 2.0))
            player.matchgoals = 0
            player.matchsaves = 0
            player.matchpasses = 0
        for player in away_players:
            player.motm = 0
            player.ssnsaves.append(round(player.matchsaves / 2.0))
            player.ssngoals.append(player.matchgoals)
            player.ssnpasses.append(round(player.matchpasses / 2.0))
            player.matchgoals = 0
            player.matchsaves = 0
            player.matchpasses = 0
        self.redcard.clear() # reset tally
        self.yellowcard.clear() # reset tally
