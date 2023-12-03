import os
import art
import bet_logic
import players

from time import sleep

hide_dealer = True


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def update(betting=False, speed=1):
    sleep(1 / speed)
    clear()

    dealer_hand = "\n\n\n\n\n\n\n\n"
    user_hand = "\n\n\n\n\n\n\n\n"

    dealer_first_card = True
    for card in players.dealer.hand:
        if dealer_first_card and hide_dealer:
            dealer_hand = art.card_back
            dealer_first_card = False
        else:
            dealer_hand = multi_line_concat(dealer_hand, card_format(card))

    for card in players.user.hand:
        user_hand = multi_line_concat(user_hand, card_format(card))

    chips_display = multi_line_concat(
        chip_format(bet_logic.total_chips, art.chips),
        chip_format(players.user.bet, art.current_bet))

    print(f"{art.logo}\n{chips_display}")

    if bet_logic.insurance_bet != 0:
        print(f"Insurance: {bet_logic.insurance_bet}")

    splits_display()

    if not betting:
        print(f"\n\nDealer's hand:{dealer_hand}\n\nYour hand:{user_hand}\n")


def splits_display():
    for split_player in players.splits:
        split_num = players.splits.index(split_player) + 1
        split_card = ''
        for card in split_player.hand:
            split_card += f"{card['rank']}{card['suit']} "
        print(
            f"Split Bet {split_num}: [ {split_player.bet} ]        Split Hand {split_num}: [ {split_card}] {split_player.status}"
        )


def card_format(card):
    if card['rank'] == '10':
        space = ''
    else:
        space = ' '
    return art.card.format(v=card['rank'], x=space, s=card['suit'])


def chip_format(chip_count, art_to_format):
    l = len(str(chip_count))
    if l > 4:
        chips_display = art_to_format.format('', '', chip_count, '', '')
    elif l > 3:
        chips_display = art_to_format.format('', '', chip_count, '', ' ')
    elif l > 2:
        chips_display = art_to_format.format(' ', '', chip_count, '', ' ')
    elif l > 1:
        chips_display = art_to_format.format(' ', '', chip_count, ' ', ' ')
    else:
        chips_display = art_to_format.format(' ', ' ', chip_count, ' ', ' ')
    return chips_display


def multi_line_concat(first_str, second_str):
    lines1 = first_str.split("\n")
    lines2 = second_str.split("\n")
    horizontal_concatenation = '\n'.join(' '.join(line)
                                         for line in zip(lines1, lines2))
    return horizontal_concatenation


def help_screen():
    clear()
    print(art.help)
    input()
    update()
