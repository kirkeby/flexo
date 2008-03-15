# -*- encoding: utf-8 -*-
import sys
import time
import socket
import traceback
import sys
import os
import logging

from pickle import dumps
from pickle import loads

from flexo.remote import Remote
from flexo.plugin import Plugin

log = logging.getLogger('flexo.irc')

reconnect_delay = 67

class Bot(object):
    __slots__ = ['server', 'address', 'nick', 'name', 'usermode',
                 'in_encodings', 'out_encoding', 'plugins', 'reason',
                 'exc_info']

    def __init__(self, address='localhost'):
        self.server = None
        self.address = address
        self.nick = u'flexo'
        self.name = u'Flexo'
        self.usermode = u'-sw'

        self.in_encodings = 'iso-8859-1', 'utf-8'
        self.out_encoding = 'iso-8859-1'

        self.reason = None
        self.exc_info = None

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
                log.exception('Network error')

            if self.reason:
                break

            time.sleep(reconnect_delay)

    def quit(self, reason):
        self.reason = 'quit'
        self.send(u'QUIT :' + reason)

    def graceful(self):
        log.info('Scheduling graceful code reload')
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
        self.network_log(u'> ' + raw)

        raw = raw.encode(self.out_encoding)
        self.server.write(raw + '\r\n')
        self.server.flush()

    def interact(self):
        while not self.reason:
            line = self.server.readline()
            if line == '':
                if not self.reason:
                    log.warning('[E] Lost connection')
                self.server = None
                break

            line = line.strip()
            for encoding in self.in_encodings:
                try:
                    line = line.decode(encoding)
                    break
                except UnicodeError:
                    pass
            else:
                log.info('[E] Could not decode %r' % line)
                continue

            self.network_log(u'< ' + line)
            try:
                self.handler(line)
            except Exception:
                self.exc_info = sys.exc_info()
                log.exception('Exception handling %r' % line)

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

    def network_log(self, txt):
        file = open('network.log', 'a')
        file.write('[%s] %s\n' % (time.asctime(), txt.encode('utf-8')))
        file.close()

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
