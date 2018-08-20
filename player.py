class Player:

    def __init__(self,nick):
        self.nick = nick        
        self.balance = 7
        self.cards = []
        self.current_bet = 0
        self.checked = False
    
    def draw_card(self,deck):
        self.cards.append(deck.get_card())

    def play_card(self,card_number):
        return self.cards.pop(card_number)

    def place_bet(self,amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            amount = self.balance
            self.balance = 0
        self.current_bet += amount
        return amount
    
    def receive_bet(self,poll):
        self.balance += poll 

    def place_starting_bet(self):
        return self.place_bet(1)

    def call_bet(self,poll):
        return self.place_bet(poll - 2 * self.current_bet)

    def raise_bet(self,amount,poll):
        return self.place_bet((poll - 2 * self.current_bet) + amount)
    
    def check(self):
        self.checked = True

    def uncheck(self):
        self.checked = False

    def end_turn(self):
        self.current_bet = 0