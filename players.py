import bet_logic
import display
import art
import os.path
import base64

from copy import deepcopy
from datetime import datetime
from time import sleep


class Player:

    def __init__(self):
        self.hand = []
        self.score = 0
        self.status = ''
        self.bet = 0
        self.initial_hand = True


dealer = Player()
user = Player()

splits = []


def init_players(only_user=False):
    global dealer, user, splits
    dealer = Player()
    user = Player()
    splits = []
    display.hide_dealer = True


def create_split():
    split = deepcopy(user)
    split.hand.pop(0)
    bet_logic.place_split_bet(split)
    splits.append(split)


def create_split_players():
    if len(splits) < 3:
        create_split()


def swap_with_split(split, keep_split=True):
    global user, splits
    copy = user
    user = split
    splits.remove(split)
    if keep_split:
        split = copy
        splits.insert(0, split)
    display.update(speed=2)


def high_scores():
    if not os.path.isfile("high_scores"):
        scores_txt = open("high_scores", "x")
        scores_txt.close()

    scores_txt = open("high_scores")

    scores = []

    for score in scores_txt.readlines():
        decoded_string = base64.b64decode(score).decode()
        split = decoded_string.split(' , ')
        date = split[0]
        name = split[1]
        score_val = int(split[2].replace("\n", ""))
        scores.append((date, name, score_val))

    scores = sorted(scores, key=lambda x: x[2])

    if len(scores) != 0:
        lowest = scores[0][2]
    else:
        lowest = 0

    if bet_logic.total_chips >= lowest or len(scores) < 10:
        display.update(speed=0.3)
        name = input(
            "\n\nNEW HIGH SCORE!\n\n\nPlease enter your name:\n ").upper()
        while not name.isalnum() or len(name) > 6:
            display.update(speed=2)
            name = input(
                "\nPlease enter up to 6 letters or numbers with no spaces!\n\nNEW HIGH SCORE!\n\n\nPlease enter your name:\n "
            ).upper()
        score = bet_logic.total_chips
        if len(scores) > 9:
            scores.pop(0)
        scores.append((datetime.now(), name, score))
        scores = sorted(scores, key=lambda x: x[2])
        with open("high_scores", "w") as scores_txt:
            for score in scores:
                string = f"{score[0]} , {score[1]} , {score[2]}\n"
                encoded_string = base64.b64encode(string.encode()).decode()
                scores_txt.write(encoded_string)
        sleep(0.5)

    else:
        print("Goodbye :)")
        sleep(4)

    display.clear()
    print(art.high_scores)
    i = 0
    for score in reversed(scores):
        i += 1
        ijust = str(i).rjust(2)
        name = score[1].rjust(6)
        print(f"  {ijust}     {name}  :  {score[2]} chips")

    input()
