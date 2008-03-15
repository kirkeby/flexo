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

class Bot(object):
    __slots__ = ['server', 'address', 'nick', 'name', 'usermode',
                 'encodings', 'log_encoding', 'out_encoding',
                 'plugins', 'reason']

    def __init__(self, address='localhost'):
        self.server = None
        self.address = address
        self.nick = u'flexo'
        self.name = u'Flexo'
        self.usermode = u'-sw'

        self.encodings = 'iso-8859-1', 'utf-8'
        self.log_encoding = 'utf-8'
        self.out_encoding = 'iso-8859-1'

        self.reason = None

        self.plugins = []

    def __getattr__(self, name):
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin
        raise KeyError(name)

    def run(self):
        while True:
            try:
                if not self.server:
                    self.connect()
                self.interact()

            except (socket.error, EnvironmentError):
                traceback.print_exc()

            if self.reason:
                break

            time.sleep(reconnect_delay)

    def quit(self, reason):
        self.reason = 'quit'
        self.send(u'QUIT :' + reason)

    def graceful(self):
        self.log('Scheduling graceful code reload')
        self.reason = 'graceful'

    def initialize(self):
        self.plugins = [Remote(self)]
        for line in open('plugins'):
            self.plugins.append(self.remote.load(line.strip()))

    def reinitialize(self, other):
        for key in other.__slots__:
            setattr(self, key, getattr(other, key))

        self.reason = None

        # FIXME - reload plugins

    def connect(self):
        assert not self.server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        self.server = s.makefile('rw')

        self.send(u'NICK %s' % self.nick)
        self.send(u'USER %s %s localhost :%s'
                  % (self.nick, self.usermode, self.name))

    def send(self, raw):
        assert isinstance(raw, unicode)
        self.log(u'> ' + raw)

        raw = raw.encode(self.out_encoding)
        self.server.write(raw + '\r\n')
        self.server.flush()

    def interact(self):
        while not self.reason:
            line = self.server.readline()
            if line == '':
                if not self.reason:
                    self.log('[E] Lost connection')
                self.server = None
                break

            line = line.strip()
            for encoding in self.encodings:
                try:
                    line = line.decode(encoding)
                    break
                except UnicodeError:
                    pass
            else:
                self.log('[E] Could not decode %r' % line)
                continue

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
