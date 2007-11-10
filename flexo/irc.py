import time
import socket
import traceback
import sys

from flexo.remote import Remote

reconnect_delay = 7

class Bot:
    def __init__(self, address):
        self.server = None
        self.address = address
        self.nick = 'flexo'
        self.name = 'Flexo'
        self.usermode = '-sw'

        self.plugins = [Ponger(self), Remote(self)]

        for line in open('plugins'):
            self.plugins.append(self.plugins[1].load(line.strip()))

    def connect(self):
        assert not self.server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        self.server = s.makefile()

        self.send('NICK %s' % self.nick)
        self.send('USER %s %s localhost :%s'
                  % (self.nick, self.usermode, self.name))

    def reconnect(self):
        self.server = None
        self.state = '-'
        time.sleep(reconnect_delay)
        self.connect()

    def send(self, raw):
        if isinstance(raw, unicode):
            self.log('> ' + raw.encode('utf-8'))
            raw = raw.encode('iso-8859-1')
        else:
            self.log('> ' + raw)

        self.server.write(raw + '\r\n')
        self.server.flush()

    def receiver(self):
        while True:
            line = self.server.readline()
            if line == '':
                self.log('Lost connection')
                self.reconnect()
                continue

            line = line.strip()
            self.log('< ' + line)

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

    def log(self, text):
        print '[%s] %s' % (time.ctime(), text)

class Ponger:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if command == 'PING':
            self.bot.send('PONG ' + rest)
            return True
