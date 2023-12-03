import random
import display
import bet_logic
import players

from copy import deepcopy

playing_splits = False
deck = []

cards = [{
    'rank': 'A',
    'value': 11
}, {
    'rank': '2',
    'value': 2
}, {
    'rank': '3',
    'value': 3
}, {
    'rank': '4',
    'value': 4
}, {
    'rank': '5',
    'value': 5
}, {
    'rank': '6',
    'value': 6
}, {
    'rank': '7',
    'value': 7
}, {
    'rank': '8',
    'value': 8
}, {
    'rank': '9',
    'value': 9
}, {
    'rank': '10',
    'value': 10
}, {
    'rank': 'J',
    'value': 10
}, {
    'rank': 'Q',
    'value': 10
}, {
    'rank': 'K',
    'value': 10
}]


def shuffle():
    spades = deepcopy(cards)
    clubs = deepcopy(cards)
    diamonds = deepcopy(cards)
    hearts = deepcopy(cards)
    suits = [[spades, '♠'], [clubs, '♣'], [diamonds, '♦'], [hearts, '♥']]

    for suit in suits:
        for card in suit[0]:
            card['suit'] = suit[1]

    deck = spades + clubs + diamonds + hearts
    return deck


def deal_card(player, debug_card=-1):
    if debug_card != -1:
        card = deck[debug_card]
    else:
        card = random.choice(deck)
        deck.remove(card)

    player.hand.append(card)

    calc_score(player)
    display.update(speed=1.5)


def initial_deal():
    display.update(speed=1.2)
    deal_card(players.user)
    deal_card(players.dealer)
    deal_card(players.user)
    deal_card(players.dealer)


def hit_me(player):
    if player == players.dealer:
        while player.score < 17:
            deal_card(player)
            display.update()
    else:
        players.user.initial_hand = False
        deal_card(player)
        display.update()


def split():
    global playing_splits
    playing_splits = True

    players.create_split_players()

    players.user.hand.pop()

    display.update(speed=0.5)
    input("Hand has been split, press ENTER to proceed.")
    display.update()

    deal_card(players.user)

    user_match = matched_cards(players.user)
    if players.user.hand[0]['rank'] != 'A':
        bet_logic.bet_controls(split=user_match)

    display.update()


def play_splits():
    for split_player in players.splits:
        players.swap_with_split(split=split_player)
        deal_card(players.user)
        user_match = matched_cards(players.user)
        bet_logic.bet_controls(split=user_match)


def calc_score(player):
    total = 0

    for card in player.hand:
        total += card['value']
    for card in player.hand:
        if card['rank'] == 'A' and total > 21:
            total -= 10
    if total == 21 and len(player.hand) == 2:
        player.status = 'blackjack'
        if playing_splits:
            display.update(speed=3)
            input("BLACKJACK!\npress ENTER to proceed.")

    if total > 21:
        player.status = 'bust'
        if playing_splits:
            display.update(speed=3)
            input("BUST!\npress ENTER to proceed.")

    player.score = total
    return total


def blackjack_check():
    if (players.user.status == 'blackjack'
            and players.dealer.status != 'blackjack'):
        difference = bet_logic.calc_bet(win=True, blackjack=True)
        display.update(speed=3)
        print('\nBLACKJACK!\nYou have a Blackjack.\nYou Win this hand at 3:2.')
        print(f"\nGained {difference} chips")
        return True

    elif players.dealer.status == 'blackjack':
        difference = bet_logic.calc_bet()
        display.update(speed=3)
        print('\nBLACKJACK!\nThe dealer has a Blackjack.\nYou Lose this hand.')
        print(f"\nLost {difference} chips")
        return True

    elif (players.user.status == 'blackjack'
          and players.dealer.status == 'blackjack'):
        difference = bet_logic.calc_bet(draw=True)
        display.update(speed=3)
        print(
            '\nBLACKJACK!\nThe dealer and you both have a Blackjack.\nIt\'s a draw.'
        )
        print(f"\n{difference} chips returned")

        return True


def bust_check():
    if players.user.status == 'bust':
        difference = bet_logic.calc_bet()
        display.update(speed=3)
        print("BUST!\nYou are bust.\nYou Lose this hand")
        print(f"\nLost {difference} chips")
        return True

    else:
        hit_me(players.dealer)

    if players.dealer.status == 'bust':
        difference = bet_logic.calc_bet(win=True)
        display.update(speed=3)
        print("BUST!\nThe dealer is bust.\nYou Win this hand!")
        print(f"\nGained {difference} chips")
        return True


def final_scores():
    if players.user.status != 'bust':
        display.hide_dealer = False
    display.update(speed=0.8)

    if blackjack_check() or bust_check():
        if playing_splits:
            input("\nScoring next split hand. Press ENTER to proceed.")
        return

    score_str = f"Dealer Score: {players.dealer.score}. Your score: {players.user.score}."

    if players.dealer.score == players.user.score:
        difference = bet_logic.calc_bet(draw=True)
        display.update()
        print(f"{score_str}\nIt's a draw!")
        print(f"\n{difference} chips returned")
    elif players.dealer.score > players.user.score:
        difference = bet_logic.calc_bet()
        display.update()
        print(f"{score_str}\nYou Lose this hand.")
        print(f"\nLost {difference} chips")

    else:
        difference = bet_logic.calc_bet(win=True)
        display.update()
        print(f"{score_str}\nYou Win this hand!")
        print(f"\nGained {difference} chips")

    if playing_splits:
        input("\nScoring next split hand. Press ENTER to proceed.")


def split_scoring():
    global playing_splits

    for split_player in reversed(players.splits):
        players.swap_with_split(split=split_player, keep_split=False)
        if len(players.splits) == 0:
            playing_splits = False

        final_scores()


def matched_cards(player):
    if (player.hand[0]['value'] == player.hand[1]['value']
            and bet_logic.total_chips >= players.user.bet
            and len(players.splits) < 3 and players.user.initial_hand):
        return True
    return False
