import card_logic
import display
import players

from math import floor

total_chips = 500
min_bet = 10
max_bet = 100

insurance_bet = 0


def place_bet(bet_amount):
    global total_chips
    players.user.bet += bet_amount
    total_chips -= bet_amount
    display.update()


def place_split_bet(player):
    global total_chips
    player.bet = players.user.bet
    total_chips -= players.user.bet


def opening_bet():
    bet = 0

    user_input = input(
        f"Place your opening bets.\n\nThe minimum is {min_bet} chips, up to a maximum of {max_bet}:\n"
    )
    if user_input == '':
        place_bet(min_bet)
        return
    try:
        bet = int(user_input)
    except:
        print("\nPlease enter a numerical value\n")
        opening_bet()
        return
    if bet < min_bet:
        print(
            f"\nPlease enter a value greater than the minimum bet of {min_bet}\n"
        )
        opening_bet()
    elif bet > total_chips:
        print(
            f"\nYou don't have enough chips! Please enter a value less than {total_chips}\n"
        )
        opening_bet()
    elif bet > max_bet:
        print(f"\nThe maximum bet is {max_bet}\n")
        opening_bet()
    else:
        place_bet(bet)


def calc_bet(win=False, draw=False, blackjack=False):
    global total_chips, insurance_bet
    chip_difference = total_chips + players.user.bet + insurance_bet

    if win:
        total_chips += 2 * players.user.bet
    if draw:
        total_chips += players.user.bet
    if blackjack:
        total_chips += floor(0.5 * players.user.bet)
    if insurance_bet and players.dealer.status == 'blackjack':
        total_chips += 3 * insurance_bet

    if total_chips != chip_difference:
        chip_difference = abs(total_chips - chip_difference)
    else:
        chip_difference = players.user.bet

    insurance_bet = 0
    players.user.bet = 0
    return chip_difference


def bet_controls(split=False, insurance=False):
    if players.user.score >= 21:
        return
        
    display.update(speed=1.2)
    
    options = [
        '<S> Stand',
        '     <H> Hit',
    ]
    if (players.user.initial_hand and total_chips > players.user.bet):
        options.append('     <D> Double Down')

    if split:
        options.append('     <X> Split')

    if (insurance and players.user.initial_hand
            and total_chips > floor(players.user.bet / 2)):
        options.append('     <I> Insurance')

    options.append('     <?> Help')

    opt_str = ""
    for option in options:
        opt_str += option
    print(opt_str)

    selection = input().lower()
    if selection == 's':
        players.user.status = 'stand'
        return
    elif selection == 'h':
        card_logic.hit_me(players.user)
        bet_controls(split=split, insurance=insurance)
    elif (selection == 'd' and players.user.initial_hand
          and total_chips > players.user.bet):
        players.user.status = 'stand'
        double_down()
    elif selection == 'x' and split:
        card_logic.split()
    elif (selection == 'i' and insurance and players.user.initial_hand
          and total_chips > floor(players.user.bet / 2)):
        take_insurance()
        display.update()
        print(
            f"\nInsurance of {insurance_bet} chips taken against possible dealer blackjack."
        )
        input("\nPress ENTER to proceed")
        display.update()
        bet_controls(split=split)
    elif selection == '?':
        display.help_screen()
        bet_controls(split=split, insurance=insurance)
    else:
        display.update()
        print("Please make a selection from the provided options.\n")
        bet_controls(split=split, insurance=insurance)


def double_down():
    place_bet(players.user.bet)
    print(f"\nDoubled bet to {players.user.bet}")
    input("\nPress ENTER to proceed")
    card_logic.hit_me(players.user)


def take_insurance():
    global insurance_bet, total_chips
    insurance_bet = floor(players.user.bet / 2)
    total_chips -= insurance_bet
