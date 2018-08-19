from myirc import *
import os
import random
from player import Player
from deck import Deck

channel = '#qwfpneio'
server = 'irc.freenode.net'
nickname ='rektixBOT'
player_nicks = []
players = []
started = False

irc = IRC()
irc.connect(server,channel,nickname)

def join_game(name):
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
    for player in list(player_nicks):
        if player == name:
            player_nicks.remove(player)
            irc.send_message(channel, name + ' has quit the game.')
    if started:        
        for player in list(players):
            if player.name == name:
                players.remove(player)   
                #game_stop() 

def show_cards(player):
    message = 'Your cards: 0[%s], 1[%s] (number[value]). Type card number to play it, not value.' % (player.cards[0].value, player.cards[1].value)
    irc.send_notice(player.nick, message)

def show_groups(player):
    if player.cards[0].group == 'UP' and player.cards[1].group == 'DOWN':
        message = '%s has %s and %s cards' % (player.nick, player.cards[1].group, player.cards[0].group)
    else:
        message = '%s has %s and %s cards' % (player.nick, player.cards[0].group, player.cards[1].group)
    irc.send_message(channel, message)

def start_turn(deck):
    players[0].draw_card(deck)
    players[1].draw_card(deck)
    show_cards(players[0])
    show_cards(players[1])
    show_groups(players[0])
    show_groups(players[1])

def start_game(name):
    if name in player_nicks:
        if len(player_nicks) == 2:
            irc.send_message(channel, 'Game started! Dealing %s as Player 1 and %s as Player 2' % (player_nicks[0], player_nicks[1]))
            deck = Deck()
            players.extend((Player(player_nicks[0]), Player(player_nicks[1])))
            players[0].draw_card(deck)
            players[1].draw_card(deck)        
            start_turn(deck)    
        else:
            irc.send_message(channel, 'Not enough players.')
    else:
        irc.send_message(channel, 'You must join a game to start it.')

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

    if ' QUIT ' in text and not ' PRIVMSG ' in text:
        name = text.split('!')[0][1:]
        player_quit(name)

    if 'PRIVMSG' in text and channel in text and "hello" in text:
        name = text.split('!')[0][1:]
        irc.send_message(channel, 'hello!'+name)

    if 'PRIVMSG' in text and channel in text:
        name = text.split('!')[0][1:]
        message = text.split('PRIVMSG ' + channel + ' :')[-1]
        if message[0] == '.':
            command = message.split(' ')[0]
            if command == '.join':
                join_game(name)
            if command == '.quit':
                player_quit(name)
            if command == '.start':
                start_game(name)