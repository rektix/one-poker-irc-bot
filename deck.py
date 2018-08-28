from random import shuffle

class Card:
    """
    A class used to represent a card in the game.

    name - display name (2-A)
    value - strength of a card (2-14)
    group - DOWN (2-7), UP(8-A)
    """

    def __init__(self,value):
        self.value = value
        if value == 14:
            self.name = 'A'
        elif value == 11:
            self.name = 'J'
        elif value == 12:
            self.name = 'Q'
        elif value == 13:
            self.name = 'K'
        else:
            self.name = str(value)

        if value < 8:
            self.group = 'DOWN'
        else:
            self.group = 'UP'

class Deck:
    """
    A class used for representing a deck in the game.

    cards - list of cards, this game uses 2 regular decks.
    """

    def __init__(self):
        self.cards = []
        for value in range(2,15):
            self.cards.append(Card(value))
        self.cards = self.cards * 8
        shuffle(self.cards)

    def get_card(self):
        """Deals card from the top of the deck"""
        return self.cards.pop()