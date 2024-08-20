# <u>Phase 10</u>
_by: GickiAnarchy_  
---
#### _development branch_
---
___<u>ToDo</u>___
-[x] Remove Stack class.  too confusing
-[x] Start Game Logic  
-[ ] Complete Game Logic  
-[x] Start GUI  
-[ ] Complete GUI  
-[ ] Start online mechanic  
-[ ] Complete Phase 10!
---

08.20.24
    Remove Stack class
    Added Discards class







## The game of Phase 10:

### Objective:
Phase 10 is a card game for 2-6 players. The goal of the game is to complete all ten phases, one round at a time. At the end of a round players will add up their score based on the number and type of cards left in their hand. The goal is to have the lowest score at the end of the game. Watch out, if you don't complete your phase in a round, you must repeat the phase in the next round!

<br>

### How to play:
During your turn you MUST draw one card to begin the turn. You can draw one of the face down cards from the pile, or draw the face up card shown. At the end of your turn you MUST discard a card, face up next to the draw pile. The turn will continue going around to the next player (generally to the left or clockwise to the person t
hat started) they will draw a card and discard a card. Note: If you ever run out of face down cards, simply flip over the face up cards to a new face down draw pile. (shuffling this new draw pile is optional, flip the top card to start a new face up draw pile)
Once a player has drawn a card to start their turn, if they have the required cards of their phase, they may choose to "lay down" their phase. The player will lay, face up, the required cards of the phase. In the picture shown the player has laid down the required cards of phase 3 (1 set of 4 and 1 run of 4). There are two important things to note about laying down a phase. You can have more than is required in your phase to lay down, and if that is the case you will want to play all cards you can, as once you complete the phase your goal becomes to discard your hand.  
__If a player has the required phase in their hand THEY ARE NOT REQUIRED to lay the phase down. The player still required to discard a card at the end of their turn.__

<br>

---
### Classes:

<br>

* _Cards_
    * Card: This class represents a single card in the game. It has properties like name, points, color, and number (derived from the name). It also defines methods for descriptions and equality comparison.
    * WildCard: This class inherits from Card and has a mimic attribute to hold the card it's mimicking. It overrides comparison operators to become the mimicked card when compared with other cards.
    * SkipCard: This class inherits from Card and has a TODO placeholder for a useSkip method.
    * BasicCard, LowCard, HighCard: These classes inherit from Card and define basic card types with specific point values.
* _Card Stacks_
    * Stack: This class represents a stack of cards. It allows adding/removing cards and sorting them by number or color.
    * Deck: This class inherits from Stack and represents the deck of cards. It has a createDeck method to populate the deck with different card types and shuffles the deck. It also allows drawing cards.
    * Hand: This class inherits from Stack and represents a player's hand of cards. It allows showing the hand's contents.
* _Phases_
    * Phase: This class represents a phase in the game. It has a number and goals (not used in the provided code).
    * PhaseGoal: This class inherits from Stack and represents a specific goal within a phase (Set, Run, or Color). It has a type (ptype) and minimum card requirement. It defines methods to check if a stack of cards meets the goal criteria and add cards to the goal stack (presumably for tracking progress). It also has methods to check for Sets, Runs, and Colors.
* _Player Logic_
    * Player: This class represents a player in the game. It has a name, hand, and a phases list (not used in the provided code). It has methods for showing the hand and discarding a card.
* _Game Logic_
    * Game: This class represents the entire Phase 10 game. It has a deck, discard pile, and list of players. It has methods to start the game (deal cards and enter a turn loop), and a turn method that simulates a player's turn (drawing a card and discarding a card).