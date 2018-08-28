# one-poker-irc-bot

This is a python IRC bot that manages game One Poker from popular manga Kaiji.

#Rules:

This game uses 2 decks of cards. Each of two players gets 2 cards and 7 coins at the beginning of the game. Cards are divided in 2 groups - DOWN (2-7) and UP (8-A). Both players know in which group opponents cards belong.After both players play their cards, betting stage begins. Players can check, raise, call or fold. When bets are over, winner is chosen. Higher value card wins, except the case where 2 beats A. Winner takes all coins from poll. Player who gets all of the coins wins.

#Commands:

.join" - join game
".quit" - quit game
".start" - start game
".cards" - shows cards
".play" - play card
".check" - check bet
".call" - call bet
".raise" - raise bet
".fold" - fold
".help" - show help
".rules" - show rules

#Setup:

Change parameters in settings.py and run bot.py script.