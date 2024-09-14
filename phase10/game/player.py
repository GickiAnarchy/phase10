

import pickle

from .cards import Card, Hand, Deck, Discards
from .phases import Phase, Goal, SetGoal, ColorGoal, RunGoal

class Player():
    """
    Represents a Player.
     
    Attributes:
        name (str): Players name.
        points (int): Players points.
        wins (int): Persistant wins
        losses (int): Persistant losses
        hand (Hand): Players hand of cards.
        phases (list): List of phases the player must complete to win the game.
        skipped (bool): Whether or not the player is going to skip their next turn.
    """
    
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.points = 0
        self.wins = 0
        self.losses = 0
        self.hand = Hand()
        self.phases = self.createPhases()
        self.skipped = False

    #   Phase Interactions
    def createPhases(self) -> list:
        """
        Creates a list of phases to complete.
        
        Returns:
            list of phases from the global variable <PHASES_DICT>.
        """
        
        p_list = []
        for k,v in PHASES_DATA.items():
            v.setOwner(self.name)
            p_list.append(v)
        print(f"10 Phases created for {self.name}")
        return p_list

    def getCurrentPhase(self) -> Phase:
        """
        Gets the players current phase by iterating through all players phases, and returns the first one that returns False as complete.
        
        Returns:
            Current phase of player
        """
        
        for phase in self.phases:
            if not phase.complete:
                return phase
        return None

    def checkCurrentPhase(self) -> bool:
        """
        Checks if the players curent phase is completed
        """
        
        return self.getCurrentPhase().complete

    def getCurrentGoals(self):
        self.getCurrentPhase().getGoals()
 
    #   Scoring
    def addPoints(self) -> int:
        """
        Add up points for cards remaining in a players hand and adds to total score.
        
        Returns:
            int: Total points of player points.
        """

        pts = 0
        for c in self.hand.cards:
            pts += c.points
        print(f"{self.name} gained {pts} points")
        self.points += pts
        return self.points

    #   Turn Actions
    def drawCard(self, card):
        """
        Add a card to players hand. 
        
        Returns:
            None
        """
        
        self.hand.addCards(card)

    def getCard(self, card) -> Card:
        """
        Gets a card from the players hand.
        
        Args:
            card: Card to search for.
        
        Returns:
            The card from a players hand.
        """
        
        ind = self.hand.getIndex(card)
        return self.hand.cards.pop(ind)
        
        def getCards(self, cards) -> list:
            """
            Gets cards from the players hand.
        
            Args:
                cards: Cards to search for.
        
            Returns:
                The card list from a players hand.
            """
        
        c_list = []
        for card in cards:
            c_list.append(self.getCard(card))
        return c_list

    def addCards(self, cards):
        self.hand.addCards(cards)

    #   Metadata
    def getPlayerData(self) -> dict:
        """
        Gathers the players data.
        
        Returns:
            Dictionary of player attributes.
        """
        
        return vars(self)
    
    def toggleSkip(self):
        """
        Toggles (true/false) the skipped attribute.
        
        Returns:
            None
        """
        
        self.skipped = not self.skipped
        print(f"{self.name} skipped = {self.skipped}")

    def checkForPlays(self) -> bool:
        """
        Checks a players currentvhand for any possible plays.
        
        Returns:
            True if a player is able to play something, otherwise it's False.
        """
        
        goals = self.getCurrentPhase().getGoals()
        ret = False
        for g in goals:
            if isinstance(g, SetGoal):
                s = self.hand.checkForSet(g.min_cards)
            if isinstance(g, RunGoal):
                r = self.hand.checkForRun(g.min_cards)
            if isinstance(g, ColorGoal):
                c = self.hand.checkForColor(g.min_cards)
            if s or r or c:
                ret = True
        return ret

    def resavePlayer(self):
        """
        Overwrites the player save in the player saves file.
        
        Returns:
            None
        """
        
        savePlayer(self, force = True)



player_saves = ".player_saves.p10"

def savePlayer(player, pin = "0000", force = False) -> bool:
    saves = getSaves()
    if player.name not in saves:
        saves[player.name] = {"data": player, "pin": pin}
    elif player.name in saves and force == True and pin == "0000":
        pin = saves[player.name]["pin"]
        saves[player.name] = {"data": player, "pin": pin}
    else:
        print("Cant save player.")
        return False
    with open(player_saves, "wb") as f:
        pickle.dump(saves, f)
    return True

def loadPlayer(name, pin):
    saves = getSaves()
    if name in saves and saves[name]["pin"] == pin:
        player_data = saves[name]["data"]
        return player_data
    else:
        print("Invalid name or PIN.")
        return None

def getSaves():
    try:
        with open(player_saves, "rb") as f:
            saves = pickle.load(f)
        return saves
    except:
        print("Error in loading saves")
        return {}





PHASES_DATA = {
    1:Phase("Phase 1", [SetGoal(3), SetGoal(3)]),
    2:Phase("Phase 2",[SetGoal(3), RunGoal(4)]),
    3:Phase("Phase 3", [SetGoal(4), RunGoal(4)]),
    4:Phase("Phase 4", [RunGoal(7)]),
    5:Phase("Phase 5", [RunGoal(8)]),
    6:Phase("Phase 6", [RunGoal(9)]),
    7:Phase("Phase 7", [SetGoal(4), SetGoal(4)]),
    8:Phase("Phase 8", [ColorGoal(7)]),
    9:Phase("Phase 9", [SetGoal(5), SetGoal(2)]),
    10:Phase("Phase 10",[SetGoal(5), SetGoal(3)]),
    11:Phase("All complete!",[])
    }