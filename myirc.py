import socket
import sys

class IRC:

    irc = socket.socket()

    def __init__(self):
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_message(self, chan, msg):
        self.irc.send(bytes('PRIVMSG %s :%s\n' %(chan,msg), 'UTF-8'))

    def send_notice(self, nick, msg):
        self.irc.send(bytes('NOTICE %s :%s \n' % (nick,msg), 'UTF-8'))        

    def connect(self, server, channel, botnick):
        print('connecting to: ' + server)
        self.irc.connect((server, 6667))
        self.irc.send(bytes('USER ' + botnick + ' ' + botnick + ' ' + botnick + ' This is bot!\n', 'UTF-8'))
        self.irc.send(bytes('NICK ' + botnick + '\n', 'UTF-8'))
        self.irc.send(bytes('JOIN ' + channel + '\n', 'UTF-8'))

    def get_text(self):
        text = self.irc.recv(2040).decode('UTF-8').strip('\n\r')

        if text.find('PING') != -1:
            self.irc.send(bytes('PONG ' + text.split() [1] + '\r\n', 'UTF-8'))

        return text 