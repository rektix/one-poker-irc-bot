class Player:

    def __init__(self,nick):
        self.nick = nick        
        self.balance = 7
        self.cards = []
        self.current_bet = 0
    
    def draw_card(self,deck):
        self.cards.append(deck.get_card())

    def play_card(self,card_number):
        return self.cards.pop(card_number)

    def place_bet(self,amount):
        if amount <= self.balance:
            self.balance -= amount
        else:
            amount = self.balance
            balance = 0
        self.current_bet += amount
        return amount
    
    def receive_bet(self,amount):
        self.balance += amount

    def place_starting_bet(self):
        return self.place_bet(1)

    def call_bet(self,poll):
        return self.place_bet(poll - 2 * self.current_bet)

    def raise_bet(self,amount,poll):
        return self.place_bet(poll - 2 * self.current_bet + amount)
    
    def end_turn(self):
        self.current_bet = 0