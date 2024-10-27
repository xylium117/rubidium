import random
import time as time
import numpy as np

from configs.odds import odds, shot_outcome
from colorama import Fore, Back, Style


class Event:
    def __init__(self, event, side, minute, player=None):
        self.event = event
        self.side = side
        self.minute = minute
        self.player = player

    def set_home_and_away_sides(self, home_side, away_side):
        self.sides = {home_side: "Home", away_side: "Away"}
        self.reverse = {home_side: away_side, away_side: home_side}

    def set_player_for_events(self, eventslist):
        attack = random.choice(
            ["defenders", "defenders", "defenders", "midfielders", "midfielders", "midfielders", "midfielders", "midfielders", "attackers", "attackers", "attackers", "attackers", "attackers", "attackers"]
        )
        card = random.choice(
            ["defenders", "defenders", "defenders", "defenders", "defenders", "defenders", "midfielders", "midfielders", "midfielders", "attackers"]
        )
        assist = random.choice(
            ["midfielders", "midfielders", "midfielders", "midfielders", "midfielders", "attackers", "attackers", "attackers", "defenders", "defenders"]
        )
        equal = random.choice(
            ["midfielders", "midfielders", "midfielders", "defenders", "defenders", "defenders", "attackers", "attackers", "attackers"]
        )
        def_players = list(eventslist[0].side.squad[card])
        atk_players = list(eventslist[0].side.squad[attack])
        mid_players = list(eventslist[0].side.squad[assist])
        base_players = list(eventslist[0].side.squad[equal])
        player = random.choice(base_players)
        for e in eventslist:
            if e.event == "Red card" or e.event == "Second yellow card" or e.event == "Yellow card" or e.event == "Blocked" or e.event == "Sending off" or e.event == "Foul":
                e.player = random.choice(def_players)
            elif e.event == "Goal" or e.event == "Attempt" or e.event == "Offside":
                e.player = random.choice(atk_players)
            elif e.event == "Corner" or e.event == "Failed through ball" or e.event == "Free kick won" or e.event == "Key Pass":
                e.player = random.choice(mid_players)
            elif e.event == "Saved":
                e.player = e.side.squad["goalkeeper"][0]
            else:
                e.player = player
        return eventslist

    def evaluate_event(self):
        if self.event == "Attempt":
            l = []
            l.append(Event(self.event, self.side, self.minute))
            attodds = []
            for oc in list(shot_outcome.keys()):
                attodds.append(shot_outcome[oc]["Probability"])
            att = random.choices(list(shot_outcome.keys()), attodds, k=1)[0]
            self.event = att
            l.append(Event(self.event, self.side, self.minute))
            if self.event == "On target":
                goalodds = []
                for g in list(shot_outcome["On target"]["is_goal"].values()):
                    goalodds.append(g)
                goal = random.choices(["Saved", "Goal"], goalodds, k=1)[0]
                if goal == "Saved":
                    self.side = self.reverse[self.side]
                self.event = goal
                l.append(Event(self.event, self.side, self.minute))
            if self.event == "Own goal":
                self.side = self.reverse[self.side]
                self.event = "Goal"
                l.append(Event(self.event, self.side, self.minute))
            l = self.set_player_for_events(l)
            return l
        elif self.event == "Foul":
            flist = []  # Foul handling below
            flist.append(Event("Foul", self.side, self.minute))
            flist.append(Event("Free kick won", self.reverse[self.side], self.minute))
            cardodds = []
            cardodds.append(
                odds[self.minute][self.sides[self.side]]["Events"]["Yellow card"]
                / odds[self.minute][self.sides[self.side]]["Events"]["Foul"]
            )
            cardodds.append(
                odds[self.minute][self.sides[self.side]]["Events"]["Red card"]
                / odds[self.minute][self.sides[self.side]]["Events"]["Foul"]
            )
            cardodds.append(1 - np.array(cardodds).sum())
            card = random.choices(["Yellow card", "Red card", "No card"], cardodds, k=1)[0]
            if card != "No card":
                flist.append(Event(card, self.side, self.minute))
            flist = self.set_player_for_events(flist)
            return flist
        else:
            l = []
            l.append(Event(self.event, self.side, self.minute))
            l = self.set_player_for_events(l)
            return l

    def show_event(self, auto, evt):
        commentary = ""
        shorten = self.player.name.split()[-1]
        if shorten == "Jr.":
            shorten = self.player.name
        if self.event == "Goal":
            s = random.choices(["SENSATIONAL GOAL!", "A BRILLIANT STRIKE!", "GOOOOAL!", "WHAT A GOAL!"], [7, 5, 10, 3], k=1)
            if s[0] == "SENSATIONAL GOAL!":
                commentary = f"{self.minute}' {s[0]} { shorten } leaves the keeper flummoxed! {self.side.name} fans are enjoying every moment of this!"
            elif s[0] == "A BRILLIANT STRIKE!":
                t = random.choices(["perfect volley", "blazing shot from distance", "perfect knuckle-ball" ])
                commentary = f"{self.minute}' {s[0]} {self.player.name} hits a {t[0]}! The keeper could do nothing about it. {self.side.name} are having a field day!"
            elif s[0] == "GOOOOAL!":
                t = random.choices(["composed finish", "tap-in", "header", "1v1"])
                if t[0] == "1v1":
                    commentary = f"{self.minute}' {s[0]} { shorten } beats the keeper and finds the net for {self.side.name} "
                else:
                    commentary = f"{self.minute}' {s[0]} { shorten } scores for {self.side.name} in a {t[0]}"
            elif s[0] == "WHAT A GOAL!":
                t = random.choices(["overhead kick", "volley", "diving header", "rabona", "backheel flick", "lob"])
                t1 = random.choices(["ext", "amaz", "pass", "impr", "sup"])
                if t1[0] == "ext":
                    commentary = f"{self.minute}' {s[0]} What a sensational {t[0]} from {self.player.name}! That is pure magic! You won't see a better goal from {self.side.name} in all season!"
                elif t1[0] == "amaz":
                    commentary = f"{self.minute}' {s[0]} Unbelievable from {self.player.name}! He's gone for the acrobatic and pulled it off in style, to the delight of the {self.side.name} fans! Absolutely stunning technique!"
                elif t1[0] == "pass":
                    commentary = f"{self.minute}' {s[0]} That is simply out of this world from {self.player.name}! A breathtaking {t[0]}, and the {self.side.name} crowd is going wild! Football at its finest!"
                elif t1[0] == "impr":
                    commentary = f"{self.minute}' {s[0]} The timing, the precision – just immaculate from {self.player.name}! A perfect {t[0]}, and the keeper had no chance. That’s a goal for the highlight reel!"
                elif t1[0] == "sup":
                    commentary = f"{self.minute}' {s[0]} I don't believe it! { shorten }'s pulled off a {t[0]} from nowhere! An audacious finish, and it’s hit the back of the net! Jubiliation from the {self.side.name} fans!"
            self.player.motm += 5
            self.player.pots += 5
            self.player.goals += 1
            self.player.matchgoals += 1
            if evt:
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
        elif self.event == "On target":
            t = random.choice([1, 2, 3])
            if t == 1:
                commentary = f"{self.minute}' SHOT! { shorten }’s hit it cleanly for {self.side.name}... and the keeper is forced into action!"
            elif t == 2:
                commentary = f"{self.minute}' SHOT! It's heading straight for goal from the shot by {self.player.name}... the goalkeeper must scramble across"
            elif t == 3:
                commentary = f"{self.minute}' SHOT! { shorten } takes the shot for {self.side.name}!"
            if evt:
                print(Fore.GREEN + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm += 3
            self.player.pots += 3
        elif self.event == "Off target":
            t = random.choice([1, 2, 3, 4, 5])
            if t == 1:
                commentary = f"{self.minute}' SHOT! {self.player.name} fails to hit the target for {self.side.name}. His teammates are disappointed in him, and they are letting him know."
            elif t == 2:
                commentary = f"{self.minute}' SHOT!  What a chance for {self.side.name}! But { shorten }'s completely miscued that, and it sails way over the bar."
            elif t == 3:
                commentary = f"{self.minute}' SHOT! {self.player.name} goes for goal for {self.side.name}! But it's well off target"
            elif t == 4:
                commentary = f"{self.minute}' SHOT! A powerful strike from {self.side.name} by { shorten }, but it's just inches past the post! That was close, but no real danger in the end."
            elif t == 5:
                commentary = f"{self.minute}' SHOT! { shorten }’s lined it up for {self.side.name}, but he's dragged it wide! A missed opportunity there."
            if evt:
                print(Fore.WHITE + Style.BRIGHT + commentary + Style.RESET_ALL)
        elif self.event == "Saved":
            s = random.choices(["STUNNING SAVE", "UNBELIEVABLE SAVE", "SAVED", "WHAT A SAVE"], [7, 5, 10, 3])
            if s[0] == "STUNNING SAVE":
                commentary = f"{self.minute}' {s[0]}! {self.player.name}, out of nowhere, pulls off a world-class save to keep {self.side.name} in the game! Unbelievable reflexes!"
            elif s[0] == "UNBELIEVABLE SAVE":
                commentary = f"{self.minute}' {s[0]}! {self.player.name} of {self.side.name} stretches like a cat to keep it out! What a save, incredible!"
            elif s[0] == "SAVED":
                commentary = f"{self.minute}' {s[0]}! {self.player.name} of {self.side.name} dives at full stretch to deny the shot! That’s absolutely sensational from the keeper!"
            elif s[0] == "WHAT A SAVE":
                commentary = f"{self.minute}' {s[0]}! {self.player.name} for {self.side.name} with an acrobatic save – how has he kept that out? Simply unbelievable!"
            if evt:
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm += 3
            self.player.saves += 1
            self.player.matchsaves += 1
            self.player.pots += 3
        elif self.event == "Blocked":
            t = random.choice([1, 2, 3, 4])
            if t == 1:
                commentary = f"{self.minute}' BLOCKED! It’s a powerful strike from {self.player.name}, but the defender steps in, and it's blocked! What a crucial intervention!"
            elif t == 2:
                commentary = f"{self.minute}' BLOCKED! { shorten } lets fly, but it’s deflected off the defender! The block might have saved them there!"
            elif t == 3:
                commentary = f"{self.minute}' BLOCKED! A fierce shot from {self.player.name}, but it’s blocked at the last second! The defender throws his body on the line to keep it out!"
            elif t == 4:
                commentary = f"{self.minute}' BLOCKED! { shorten } pulls the trigger, but it’s deflected off a defender – and the goalkeeper is completely wrong-footed! Lucky escape!"
            if evt:
                print(Fore.BLUE + commentary + Style.RESET_ALL)
            self.player.motm += 1
            self.player.pots += 1
        elif self.event == "Hit the bar":
                t = random.choice(["a thunderous shot", "a fantastic effort", "a close call"])
                t1 = random.choice(["hits the woodwork", "crashes off the bar"])
                commentary = f"{self.minute}' { shorten } strikes {t} for {self.side.name}, but it {t1}! So close!"
                if evt:
                    print(Fore.RED + commentary + Style.RESET_ALL)
                self.player.motm += 1
                self.player.pots += 1
        elif self.event == "Attempt":
            commentary = f"{self.minute}' SHOT! { shorten } attempts a shot for {self.side.name}. This might give them an advantage!"
            if evt:
                print(Fore.GREEN + Style.DIM + commentary + Style.RESET_ALL)
        elif self.event == "Corner":
            commentary = f"{self.minute}' {self.side.name} has won a corner! { shorten } will take it. This could be dangerous!"
            if evt:
                print(Fore.CYAN + Style.DIM + commentary + Style.RESET_ALL)
        elif self.event == "Failed through ball":
            commentary = f"{self.minute}' { shorten } tries a through ball, but it's intercepted! {self.side.name} can't find a way through!"
            if evt:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
        elif self.event == "Foul":
            commentary = f"{self.minute}' FOUL! A foul by {self.player.name} gives away a free kick! The referee had no hesitation in blowing the whistle."
            if evt:
                print(Fore.WHITE + Style.BRIGHT + commentary + Style.RESET_ALL)
        elif self.event == "Free kick won":
            commentary = f"{self.minute}' { shorten } wins a free kick for {self.side.name}. This could be a good opportunity!"
            if evt:
                print(Fore.LIGHTCYAN_EX + Style.DIM +  commentary + Style.RESET_ALL)
            self.player.motm += 1
            self.player.pots += 1
        elif self.event == "Hand ball":
            commentary = f"{self.minute}' Handball! { shorten } is penalized for a handball. Free kick awarded to the opposition."
            if evt:
                print(Fore.YELLOW + Style.DIM + commentary + Style.RESET_ALL)
        elif self.event == "Key Pass":
            commentary = f"{self.minute}' A key pass from {self.player.name}! That could open up the defense for {self.side.name}!"
            if evt:
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm += 2
            self.player.pots += 2
            self.player.keypasses += 1
            self.player.matchpasses += 1
        elif self.event == "Offside":
            commentary = f"{self.minute}' OFFSIDE! { shorten } is caught offside! The linesman raises the flag."
            if evt:
                print(Fore.LIGHTMAGENTA_EX + commentary + Style.RESET_ALL)
        elif self.event == "Own goal":
            commentary = f"{self.minute}' OWN GOAL! Oh no! An own goal by {self.player.name}! That's a disaster for {self.side.name}!"
            if evt:
                print(Fore.RED + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm -= 3
            self.player.pots -= 3
        elif self.event == "Penalty Conceded":
            commentary = f"{self.minute}' { shorten } concedes a penalty! A huge moment in the match for {self.side.name}!"
            if evt:
                print(Fore.RED + Style.BRIGHT + commentary + Style.RESET_ALL)
        elif self.event == "Red card":
            commentary = f"{self.minute}' RED CARD! { shorten } is sent off for {self.side.name}! That could change everything!"
            if evt:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm -= 2
            self.player.pots -= 2
            self.player.red += 1
        elif self.event == "Second yellow card":
            commentary = f"{self.minute}' SECOND YELLOW CARD! { shorten } is given his marching orders! A foolish mistake for {self.side.name}!"
            if evt:
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm -= 2
            self.player.pots -= 2
            self.player.red += 1
        elif self.event == "Yellow card":
            commentary = f"{self.minute}' YELLOW CARD! { shorten } is booked for his first offense! He needs to be careful now for {self.side.name}."
            if evt:
                print(Fore.LIGHTYELLOW_EX + commentary + Style.RESET_ALL)
            self.player.motm -= 1
            self.player.pots -= 1
            self.player.yellow += 1
        elif self.event == "Substitution":
            commentary = f"{self.minute}' {self.side.name} is making a substitution! {self.player.name} comes off"
            if evt:
                print(Fore.MAGENTA + commentary + Style.RESET_ALL)
        elif self.event == "Sending off":
            commentary = f"{self.minute}' { shorten } is given his marching orders! A foolish mistake for {self.side.name}!"
            if evt:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + commentary + Style.RESET_ALL)
            self.player.motm -= 2
            self.player.pots -= 2
            self.player.red += 1

        if auto:
            time.sleep(0.1)
        else:
            time.sleep(0)
