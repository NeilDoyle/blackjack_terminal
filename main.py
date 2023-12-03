import bet_logic
import card_logic
import display
import players
import os


def blackjack():
    players.init_players()
    card_logic.deck = card_logic.shuffle()

    display.update(betting=True)
    bet_logic.opening_bet()
    card_logic.initial_deal()

    user_match = card_logic.matched_cards(players.user)

    dealer_ace = False
    if players.dealer.hand[1]['rank'] == 'A':
        dealer_ace = True

    bet_logic.bet_controls(split=user_match, insurance=dealer_ace)
    card_logic.play_splits()

    card_logic.final_scores()
    card_logic.split_scoring()

    if bet_logic.total_chips < bet_logic.min_bet:
        print(
            "\nYou don't have enough chips to continue, better luck next time!"
        )
        new_round = 'n'
    else:
        new_round = input(
            "\nWould you like to play another round? Y/N  ").lower()

    if new_round == 'y' or new_round == '':
        blackjack()
    else:
        print(f"\n\nYou are leaving with {bet_logic.total_chips} chips.")
        players.high_scores()


if os.name == 'nt':
    os.system('mode 80,52')
    os.system('color 0a')
else:
    os.system('stty cols 80 rows 52')
    os.system('tput setaf 2')
    
blackjack()
