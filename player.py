class Player:
    """
    A class that contains information about player.

    nick - nickname of the user
    balance - current balance in coins
    cards - list of cards in hand
    current_bet - tracks bet in current round
    checked - has player checked 
    """

    def __init__(self,nick):
        self.nick = nick        
        self.balance = 7
        self.cards = []
        self.current_bet = 0
        self.checked = False
    
    def draw_card(self,deck):
        """Receives a card into the hand.
        
        card - received card
        """

        self.cards.append(deck.get_card())

    def play_card(self,card_number):
        """"Plays selected card.

        card_number - index of selected card in hand
        """

        return self.cards.pop(card_number)

    def place_bet(self,amount):
        """Adds coins from player's balance to the winning poll.

        amount - amount of coins to bet.
        """

        if amount <= self.balance:
            self.balance -= amount
        else:
            amount = self.balance
            self.balance = 0
        self.current_bet += amount
        return amount
    
    def receive_bet(self,poll):
        """Receives winnings.
        
        poll - current amount of coins in winning poll
        """

        self.balance += poll 

    def place_starting_bet(self):
        """Places initial bet (1 coin)."""

        return self.place_bet(1)

    def call_bet(self,poll):
        """Follows opponent's bet.

        poll - current amount of coins in winning poll
        """

        return self.place_bet(poll - 2 * self.current_bet)

    def raise_bet(self,amount,poll):
        """Raises bet by selected amount.
        
        amount - amount of coins to raise
        poll - current amount of coins in winning poll
        """
        return self.place_bet((poll - 2 * self.current_bet) + amount)
    
    def check(self):
        """Sets checked flag to true."""

        self.checked = True

    def uncheck(self):
        """Sets checked flag to false."""

        self.checked = False

    def end_turn(self):
        """Resets player's bet."""
        
        self.current_bet = 0