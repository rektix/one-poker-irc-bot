"""
One Poker IRC bot 

This bot acts as a dealer for the game One Poker. 
"""
from myirc import IRC
import os
import random
from player import Player
from deck import Deck
import settings

#initializing global variables
channel = settings.channel
server = settings.server
nickname = settings.nickname
player_nicks = []
players = []
started = False
played_cards = [None,None]
waiting_for_cards = False
betting_started = False
poll = 0
turn = 0
last_action = ''
deck = Deck()
irc = IRC()

def show_help():
    """Shows bot commands as a message to the channel."""

    irc.send_message(channel, 'List of commands: ".join" - join game, ".quit" - quit game, ".start" - start game, ".cards" - shows cards, ".play" - play card, ".check" - check bet, ".call" - call bet, ".raise" - raise bet, ".fold" - fold, ".help" - show help, ".rules" - show rules.')

def show_rules():
    """Shows game rules as a message to the channel."""

    irc.send_message(channel, 'One Poker rules - This is a card game from manga "Kaiji". It uses 2 decks of cards. Each of two players gets 2 cards and 7 coins at the beginning of the game. Cards are divided in 2 groups - DOWN (2-7) and UP (8-A). Both players know in which group opponents cards belong.')
    irc.send_message(channel, 'After both players play their cards, betting stage begins. Players can check, raise, call or fold. When bets are over, winner is chosen. Higher value card wins, except the case where 2 beats A. Winner takes all coins from poll. Player who gets all of the coins wins.')

def join_game(name):
    """Adds user to the game session, displays proper message if that is not possible.
     
    name - nickname of a user
    """

    global started
    if not started:
        if name in player_nicks:
            irc.send_message(channel, name + ', you are already in the game.')
        elif len(player_nicks) == 0:
            irc.send_message(channel, name + ' has joined the game! One more player needed!')
            player_nicks.append(name)
        elif len(player_nicks) == 1:
            irc.send_message(channel, name + ' has joined the game! We have enough players! Type ".start" to start!')
            player_nicks.append(name)
        elif len(player_nicks) == 2:
            irc.send_message(channel,'Sorry, both seats are already taken, please wait for the next round')
    else:
        irc.send_message(channel, 'Game has already started.')
    players_string = ''
    for player in player_nicks:
        players_string += player + ', '
    irc.send_message(channel, 'Players in game: ' + players_string[:-2])

def player_quit(name):
    """Removes player from game session.
    
    name - nickname of a user
    """

    global started
    for player in list(player_nicks):
        if player == name:
            player_nicks.remove(player)
            irc.send_message(channel, name + ' has quit the game.')
    if started == True:        
        for player in list(players):
            if player.nick == name:                  
                game_stop()
                break 

def game_stop():
    """Stops the game."""

    global started, players
    players = list()
    irc.send_message(channel, 'Game stopped!')  
    started = False              

def show_cards(player):
    """Sends notice to the player containing their cards.
    
    player - player object of selected player
    """

    message = 'Your cards: 0[%s], 1[%s] (number[value]). Type card number to play it, not value.' % (player.cards[0].name, player.cards[1].name)
    irc.send_notice(player.nick, message)

def show_groups(player):
    """Shows card groups for player's cards.
    
    player - player object of selected player
    """

    if player.cards[0].group == 'UP' and player.cards[1].group == 'DOWN':
        message = '%s has %s and %s cards' % (player.nick, player.cards[1].group, player.cards[0].group)
    else:
        message = '%s has %s and %s cards' % (player.nick, player.cards[0].group, player.cards[1].group)
    irc.send_message(channel, message)

def show_poll():
    """Shows coins in reward poll."""

    irc.send_message(channel, 'Winning poll: %s coins' % poll)

def show_balance():
    """Shows balance of both players."""

    irc.send_message(channel, '%s has %s coins. %s has %s coins.' % 
                    (player_nicks[0],players[0].balance,player_nicks[1],players[1].balance))

def start_game(name):
    """Starts game if player that ran command is in game session.
    
    name - nickname of a user
    """
    global started, poll, deck
    if started == True:
        irc.send_message(channel, 'Game already started.')
    elif name in player_nicks:
        if len(player_nicks) == 2:
            started = True
            irc.send_message(channel, 'Game started! Dealing %s as Player 1 and %s as Player 2' % (player_nicks[0], player_nicks[1]))
            deck = Deck()
            poll = 0
            players.extend((Player(player_nicks[0]), Player(player_nicks[1])))
            players[0].draw_card(deck)
            players[1].draw_card(deck)              
            start_round()    
        else:
            irc.send_message(channel, 'Not enough players.')
    else:
        irc.send_message(channel, 'You must join a game to start it.')

def turn_to_bet():
    """Shows whose turn to bet is."""

    player = player_nicks[turn]
    irc.send_message(channel, player + '\'s turn to bet.')

def start_round(winner=''):
    """Starts game round.
    
    winner - player who won last game
        - if its value is 'tie', players won't put starting bet again
    """

    global waiting_for_cards, last_action, poll
    played_cards[0] = None
    played_cards[1] = None
    players[0].uncheck()
    players[1].uncheck() 
    players[0].end_turn()
    players[1].end_turn()
    if not winner == 'tie':
        poll += players[0].place_starting_bet()      
        poll += players[1].place_starting_bet()  
    if winner == players[0]:
        players[0].draw_card(deck)
        players[1].draw_card(deck)
    else:
        players[1].draw_card(deck)
        players[0].draw_card(deck)
    show_cards(players[0])
    show_cards(players[1])
    show_groups(players[0])
    show_groups(players[1])
    show_balance()
    show_poll()
    waiting_for_cards = True   
    last_action = ''

def play_card(name,card):
    """Plays selected card if player is in the game.
    
    name - nickname of a user
    card - index of selected card
    """

    global waiting_for_cards
    if waiting_for_cards and started:
        if name in player_nicks and card in [0,1]:
            for i in players:
                if i.nick == name:
                    player = i
                    break
            index = players.index(player)
            if played_cards[index] is None:
                played_cards[index] = player.play_card(card)
                irc.send_message(channel, player.nick + ' played a card.')
                if played_cards[0] is not None and played_cards[1] is not None:
                    waiting_for_cards = False
                    start_betting_round()
            else:
                irc.send_message(channel, 'You have already played your card.')
        elif name not in player_nicks:
            irc.send_message(channel, 'You are not in game.')
        else:
            irc.send_message(channel, 'Invalid card')
    else:
        irc.send_message(channel, 'Not time to play yet!')

def start_betting_round():
    """Starts betting round"""

    global betting_started
    irc.send_message(channel, 'Both cards played, betting starts!')
    betting_started = True
    turn_to_bet()
    if players[0].balance == 0 or players[1].balance == 0:
        showdown()

def player_check(name):
    """Player checks if all conditions are satisfied, otherwise displays proper message.
    
    name - nickname of a user
    """

    global turn, last_action
    if betting_started:
        player = players[turn]
        if player.nick == name:
            if not last_action == 'raise all':
                if  not last_action == 'raise':        
                    player.check()
                    irc.send_message(channel, player.nick + ' checks.')
                    show_balance()
                    show_poll()
                    last_action = 'check'
                    turn = 1 if turn == 0 else 0
                    if players[0].checked and players[1].checked:
                        showdown()
                    else:
                        turn_to_bet()
                else:
                    irc.send_message(channel, 'You can call, raise or fold.')
            else:
                irc.send_message(channel, 'You can call or fold.')
        else:
            irc.send_message(channel, 'It\'s not your turn to bet.')            
    else:
        irc.send_message(channel, 'Betting round hasn\'t started yet.')

def player_raise(name,amount):
    """Player raises if all conditions are satisfied, otherwise displays proper message.
    
    name - nickname of a user
    amount - raise amount
    """

    global poll, turn, last_action
    if betting_started:
        player = players[turn]
        if player.nick == name:
            if amount > 0:            
                if amount > players[0].balance:
                    amount = players[0].balance
                if amount > players[1].balance:
                    amount = players[1].balance
                poll += player.raise_bet(amount,poll)
                irc.send_message(channel, player.nick + ' raised!')
                player.uncheck()
                show_balance()
                show_poll()
                last_action = 'raise'
                turn = 1 if turn == 0 else 0    
                if player.balance == 0:
                    last_action = 'raise all'
                    irc.send_message(channel, name + ' goes all in!!!')
                    player.check()                
                turn_to_bet()
            else:
                irc.send_message(channel, 'Please enter positive amount.')                
        else:
            irc.send_message(channel, 'It\'s not your turn to bet.')
    else:
        irc.send_message(channel, 'Betting round hasn\'t started yet.')

def player_call(name):
    """Player calls if all conditions are satisfied, otherwise displays proper message.
    
    name - nickname of a user
    """

    global poll, turn, last_action
    if betting_started:
        player = players[turn]
        if player.nick == name:
            if not last_action == 'check':
                poll += player.call_bet(poll)
                irc.send_message(channel, player.nick + ' calls.')
                player.uncheck()
                show_balance()
                show_poll()                
                turn = 1 if turn == 0 else 0    
                if player.balance == 0:
                    irc.send_message(channel, name + ' goes all in!!!')
                    players[0].check()
                    players[1].check()                    
                    showdown()
                elif last_action == 'raise all':
                    players[0].check()
                    players[1].check()                    
                    showdown()
                else:
                    turn_to_bet()
                last_action = 'call'
            else:
                irc.send_message(channel, 'You can check, raise or fold.')            
        else:
            irc.send_message(channel, 'It\'s not your turn to bet.')
    else:
        irc.send_message(channel, 'Betting round hasn\'t started yet.')

def player_fold(name):
    """Player folds if all conditions are satisfied, otherwise displays proper message.
    
    name - nickname of a user
    """

    global poll, turn
    if betting_started:
        player = players[turn]
        if player.nick == name:
            irc.send_message(channel, player.nick + ' folds.')
            player.uncheck()
            turn = 1 if turn == 0 else 0
            winner = players[turn]        
            end_round(winner)    
        else:
            irc.send_message(channel, 'It\'s not your turn to bet.')
    else:
        irc.send_message(channel, 'Betting round hasn\'t started yet.')

def showdown():
    """Proceeds round to showdown phase, determines the winner."""

    global betting_started
    irc.send_message(channel, 'SHOWDOWN!')
    irc.send_message(channel, '%s played %s' % (player_nicks[0],played_cards[0].name))
    irc.send_message(channel, '%s played %s' % (player_nicks[1],played_cards[1].name))
    if played_cards[0].value == 2 and played_cards[1].value == 14:
        winner = players[0]
    elif played_cards[0].value == 14 and played_cards[1].value == 2:
        winner = players[1]
    elif played_cards[0].value > played_cards[1].value:
        winner = players[0]
    elif played_cards[0].value < played_cards[1].value:
        winner = players[1]
    else:
        winner = 'tie'
    betting_started = False
    end_round(winner)

def end_round(winner):
    """Sends winnings to the winner, starts next round.
    
    winner - player object of the winner
    """

    if not winner == 'tie':
        global poll        
        winner.receive_bet(poll)
        irc.send_message(channel, '%s won %s coins!' % (winner.nick,str(poll)))        
        poll = 0
        if players[0].balance == 0:
            end_game(1)
        elif players[1].balance == 0:
            end_game(0)
        else: start_round(winner)
    else:
        irc.send_message(channel, 'It\'s a tie!')
        start_round(winner)

def end_game(winner):
    """Ends game, declares winner.
    
    winner - index of winner's nickname
    """

    global started, players, player_nicks
    irc.send_message(channel, player_nicks[winner] + ' won the game!!!')
    started = False
    players = list()
    player_nicks = list()
    
def main():
    """Connects bot to the server, receives commands and responds to them."""

    irc.connect(server,channel,nickname)
    while 1:
        text = irc.get_text()
        print(text)

        if 'NICK' in text and channel in text:
            old_nick = text.split('!')[0][1:]
            new_nick = message = text.split('NICK ' + channel + ' :')[-1]
            for player in player_nicks:
                if player == old_nick:
                    player = new_nick
            for player in players:
                if player.nick == old_nick:
                    player.nick = new_nick

        if (' QUIT ' in text or ' PART ' in text) and not ' PRIVMSG ' in text:
            name = text.split('!')[0][1:]
            player_quit(name)

        if 'PRIVMSG' in text and channel in text:
            name = text.split('!')[0][1:]
            message = text.split('PRIVMSG ' + channel + ' :')[-1]
            if message[0] == '.':
                command = message.split(' ')[0]
                if command == '.join':
                    join_game(name)
                elif command == '.quit':
                    player_quit(name)
                elif command == '.start':
                    start_game(name)
                elif command == '.cards':
                    if started and name in player_nicks:
                        for player in players:
                            if player.nick == name:
                                name = player
                                break                    
                        show_cards(name)
                elif command == '.play':
                    try:
                        card = int(message.split(' ')[1])
                        play_card(name, card)
                    except:
                        irc.send_message(channel, 'Nothing to play.')                
                elif command =='.check':                
                    player_check(name)
                elif command == '.call':
                    player_call(name)
                elif command == '.raise':
                    try:
                        amount = int(message.split(' ')[1])
                        player_raise(name,amount)                    
                    except:
                        irc.send_message(channel, 'Please enter raise amount.')        
                elif command == '.fold':
                    player_fold(name)
                elif command == '.help':
                    show_help()
                elif command == '.rules':
                    show_rules()
                else:
                    irc.send_message(channel, 'Invalid command, for help type ".help", for rules type ".rules"')

if __name__ == '__main__':
    main()