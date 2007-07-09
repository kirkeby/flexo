import socket
import traceback
import sys

from flexo.remote import Remote

class Bot:
    def __init__(self, address):
        self.server = None
        self.address = address
        self.nick = 'flexo'

        self.plugins = [Ponger(self), Remote(self)]

    def connect(self):
        assert not self.server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        self.server = s.makefile()

        self.send('NICK %s' % self.nick)
        self.send('USER %s sune-laptop localhost :Flexo The Bot' % self.nick)

    def send(self, raw):
        print '[>] ' + raw
        self.server.write(raw + '\r\n')
        self.server.flush()

    def receiver(self):
        while True:
            line = self.server.readline()
            if line == '':
                print '[E] Lost connection'
                self.server = None
                self.state = '-'
                return
            line = line.strip()

            try:
                self.handler(line)
            except:
                traceback.print_exc()

    def handler(self, line):
        if line.startswith(':'):
            sender, command, rest = line.split(' ', 2)
        else:
            sender = None
            command, rest = line.split(' ', 1)

        for plugin in self.plugins:
            try:
                if plugin.handle(sender, command, rest):
                    break
            except:
                traceback.print_exc()
        else:
            print '[U] ' + line

class Ponger:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if command == 'PING':
            self.bot.send('PONG ' + rest)
            return True
