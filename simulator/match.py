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
        self.redcard = []
        self.yellowcard = []
        self.evt = evt
        self.hscore = 0
        self.ascore = 0

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
                elif event.event == "Yellow Card":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                elif event.event == "Red Card":
                    event_data.append([event.player.name + " (RED CARD)", timestamp, ""])
                elif event.event == "Offside":
                    event_data.append([event.player.name + " (" + event.event.upper() + ")", timestamp, ""])
                elif event.event == "On Target":
                    onTargetA += 1
                elif event.event == "Blocked":
                    onTargetA += 1
                elif event.event == "Attempt":
                    shotA += 1
                elif event.event == "Key Pass" or event.event == "Free kick won" or event.event == "Corner":
                    posA += 35
            elif event.side == self.away_side:  # Player B is left aligned
                if event.event == "Goal":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    onTargetB += 1
                elif event.event == "Own goal":
                    event_data.append([event.player.name + " (O.G)", timestamp, ""])
                    self.home_goals += 1
                elif event.event == "Saved":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                    onTargetA += 1
                elif event.event == "Yellow Card":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
                elif event.event == "Red Card":
                    event_data.append(["", timestamp, event.player.name + " (RED CARD) "])
                elif event.event == "Offside":
                    event_data.append(["", timestamp, event.player.name + " (" + event.event.upper() + ")"])
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
        total = pA + pB
        if total == 0:  # Prevent division by zero
            teamA_length = 0
            teamB_length = 30
        else:
            teamA_length = int(30 * (pA / total))
            teamB_length = 30 - teamA_length
        possession_bar = f"[{'█' * teamA_length}{'░' * teamB_length}]"

        total = shotA + shotB
        if total == 0:  # Prevent division by zero
            teamA_length = 0
            teamB_length = 30
        else:
            teamA_length = int(30 * (shotA / total))
            teamB_length = 30 - teamA_length
        shots_bar = f"[{'█' * teamA_length}{'░' * teamB_length}]"
        # display stats
        stats = [
            [f"Possession: {pA}", possession_bar, f"{pB}"],
            [f"Shots: {shotA}({onTargetA})", shots_bar, f"{shotB}({onTargetB})"]
        ]

        # Print the stats section
        print(tabulate(stats, tablefmt="plain", numalign="center", stralign="center", showindex=False, headers=[self.home_side.name.upper(), f"{self.home_goals}  -  {self.away_goals}", self.away_side.name.upper()]))
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
        self.redcard = [] # reset tally
        self.yellowcard = [] # reset tally