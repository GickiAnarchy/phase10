


from cards import Hand, Card
from phases import Goal, Phase, SetGoal, RunGoal, ColorGoal
#from phase10 import PHASES_DATA


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
        self.wins, self.losses = 0
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
        for k,v in PHASES_DICT.items():
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
 
    #   Scoring
    def addPoints(self) -> int:
        """
        Add up points for cards remaining in a players hand and adds to total score.
        
        Returns:
            int: Total points of player points.
        """
        
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
        print(f"{self.name} skipped")

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

