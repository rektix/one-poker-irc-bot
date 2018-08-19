from random import shuffle

class Card:
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
            self.group = 'down'
        else:
            self.group = 'up'

class Deck:
    def __init__(self):
        self.cards = []
        for value in range(2,15):
            self.cards.append(Card(value))
        self.cards = self.cards * 8
        shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()