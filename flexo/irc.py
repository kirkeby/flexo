# -*- encoding: utf-8 -*-
import time
import socket
import traceback
import sys
import os
from pickle import dumps
from pickle import loads

from flexo.remote import Remote
from flexo.plugin import Plugin

reconnect_delay = 67

class Bot:
    def __init__(self, address='localhost'):
        self.server = None
        self.address = address
        self.nick = u'flexo'
        self.name = u'Flexo'
        self.usermode = u'-sw'

        self.encodings = 'iso-8859-1', 'utf-8'
        self.log_encoding = 'utf-8'
        self.out_encoding = 'iso-8859-1'

        self.remote = Remote(self)
        self.plugins = [self.remote]

    def initialize(self):
        for line in open('plugins'):
            self.plugins.append(self.remote.load(line.strip()))

    def reinitialize(self, state):
        for name, state in loads(state):
            plugin = self.remote.load(name)
            plugin.set_state(state)
            self.plugins.append(plugin)

        self.log('Reinitialized %d plugins' % len(self.plugins))

    def graceful(self):
        assert self.server
        fd = str(self.server.fileno())
        state = dumps([(plugin.name, plugin.get_state())
                       for plugin in self.plugins[1:]])
        argv = [sys.executable, __file__, '--graceful', fd, state]
        os.execv(sys.executable, argv)

    def connect(self):
        assert not self.server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        self.server = s.makefile('rw')

        self.send(u'NICK %s' % self.nick)
        self.send(u'USER %s %s localhost :%s'
                  % (self.nick, self.usermode, self.name))

    def reconnect(self):
        self.server = None
        self.state = '-'
        time.sleep(reconnect_delay)
        self.connect()

    def send(self, raw):
        assert isinstance(raw, unicode)
        self.log(u'> ' + raw)

        raw = raw.encode(self.out_encoding)
        self.server.write(raw + '\r\n')
        self.server.flush()

    def receiver(self):
        while True:
            line = self.server.readline()
            if line == '':
                self.log('[E] Lost connection')
                self.reconnect()
                continue

            line = line.strip()
            for encoding in self.encodings:
                try:
                    line = line.decode(encoding)
                    break
                except UnicodeError:
                    pass
            else:
                self.log('[E] Could not decode %r' % line)
                return

            self.log(u'< ' + line)
            try:
                self.handler(line)
            except:
                traceback.print_exc()

    def parse_line(self, line):
        sender, rest = line.split(u' ', 1)
        if u':' in rest:
            before, after = rest.split(u':', 1)
            pieces = before.split()
            pieces.append(after)
        else:
            pieces = rest.split(u' ')

        command = pieces.pop(0)
        return Message(self, sender, command, pieces)

    def handler(self, line):
        if line.startswith(u'NOTICE '):
            return
        if line.startswith(u'PING '):
            self.send(line.replace('PING', 'PONG'))
            return

        message = self.parse_line(line)
        for plugin in self.plugins:
            if plugin.handle(message):
                break

    def log(self, text):
        text = text.encode('utf-8', 'ignore')
        line = '[%s] %s' % (time.ctime(), text)
        print line

class Message:
    def __init__(self, bot, sender, command, rest):
        self.bot = bot
        self.sender = sender

        if sender.startswith(u':') and u'!' in sender:
            self.nick = sender.split(u'!', 1)[0][1:]
        else:
            self.nick = None
        
        self.command = command
        self.rest = rest

        self.channel = self.bot.channels.get(rest[0])
        self.tail = rest[-1]

    def reply(self, what):
        if self.channel and self.nick:
            self.bot.send(u'PRIVMSG %s :%s, %s'
                          % (self.channel.name, self.nick, what))
        elif self.nick:
            self.bot.send(u'PRIVMSG %s :%s' % (self.nick, what))
    def reply_action(self, what):
        if self.channel:
            self.bot.send(u'PRIVMSG %s :\x01ACTION %s\x01'
                          % (self.channel.name, what))
        elif self.nick:
            self.bot.send(u'PRIVMSG %s :\x01ACTION %s\x01'
                          % (self.nick, what))

if __name__ == '__main__':
    if len(sys.argv) == 4 and sys.argv[1] == '--graceful':
        s = socket.fromfd(int(sys.argv[2]), socket.AF_INET, socket.SOCK_STREAM)
        server = socket._fileobject(s)

        state = sys.argv[3]

        flexo = Bot()
        flexo.reinitialize(state)
        flexo.server = server
        flexo.log('[I] Gracefully restarted')
        flexo.receiver()
