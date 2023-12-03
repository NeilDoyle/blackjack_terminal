logo = """
.------.            _     _            _    _            _    
|A_  _ |.          | |   | |          | |  (_)          | |   
|( \/ ).-----.     | |__ | | __ _  ___| | ___  __ _  ___| | __
| \  /|K /\  |     | '_ \| |/ _` |/ __| |/ / |/ _` |/ __| |/ /    
|  \/ | /  \ |     | |_) | | (_| | (__|   <| | (_| | (__|   <     
`-----| \  / |     |_.__/|_|\__,_|\___|_|\_\ |\__,_|\___|_|\_\\    
      |  \/ K|                            _/ |                    
      `------'                           |__/                     
      
"""

card = """
.-------.
|{v}{x}     |
|       |
|   {s}   |
|       |
|     {x}{v}|
`-------'
"""

card_back = """
 .-------.
 ||\/\/\||
 ||/\/\/||
 ||\/\/\||
 ||/\/\/||
 ||\/\/\||
 `-------'
"""

chips = """
  .-----.    
 / .---. \   
|||{}{}{}{}{}|||  
 \ `---' /   
  `-----'    
"""

current_bet = """
 __________    
|Current /\|   
|/\{}{}{}{}{} \/|   
|\/    Bet |   
 ----------    
"""

help = """
========================================
            BLACKJACK HELP
========================================

AIM OF THE GAME:
----------------
   The goal is to have a hand value closer to 21 than the dealer, 
   without exceeding 21.

   King, Queen, Jack and 10 are all worth 10
   Ace is worth 11, though its value is reduced to 1 
   if 11 would make you go BUST

   - BUST: Exceeding 21 points. A busted hand loses the round. If both 
   the player and dealer are BUST, the player still loses.

   - BLACKJACK: A hand with just an Ace and any 10-value card is a blackjack,
                which pays out at 3:2 unless the dealer also has blackjack.

OPTIONS:
--------
   <S> Stand       - End your turn without drawing another card, w
                        final scores will be calculated.
   <H> Hit         - Draw another card from the deck.
   <D> Double Down - Double your bet and draw another card. 
                        You may not draw any more cards in this hand.
   <X> Split       - If you have a pair, split them into two separate hands.
   <I> Insurance   - If the dealer is showing an Ace, place an additional bet 
                        of half of your current bet which is paid out at 2:1.

NOTE:
-----
   - You can only Double Down on your initial hand.
   - Split is available only if you have a pair.
   - Split can done up to 3 times per game. 
   - Each split places an additional bet equal to the Current bet
   - Insurance is offered when the dealer's up card is an Ace.
   - If the dealer has a Blackjack, Insurance essentially 
        prevents you from losing any chips.

========================================
"""

high_scores = """
========================================
        BLACKJACK HIGH SCORES
========================================
"""

## TODO: colours, sounds
## TODO: card suit symbol grid
