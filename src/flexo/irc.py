# -*- encoding: utf-8 -*-

from __future__ import absolute_import

import sys
import time
import socket
import logging
import imp

from flexo.plugin import Plugin

log = logging.getLogger('flexo.irc')

reconnect_delay = 67
timeout = 180
max_timeouts = 2

class Plugins(object):
    __slots__ = '_names', '_plugins', '_bot'

    def __init__(self, bot):
        self._bot = bot
        self._names = []
        self._plugins = {}

    def __getattr__(self, name):
        return self._plugins[name]
    def __iter__(self):
        return iter(self._plugins[name] for name in self._names)

    def imp(self, name):
        path = 'src/plugins/%s.py' % name
        file = open(path, 'r')
        description = '.py', 'r', imp.PY_SOURCE
        try:
            module = imp.load_module(name, file, path, description)
        except:
            file.close()
            raise

        klass = module.plugin
        plugin = klass(self._bot)
        plugin.name = name

        return plugin

    def load(self, name):
        replacement = self.imp(name)
        if self._plugins.has_key(name):
            replacement.set_state(self._plugins[name].get_state())
        else:
            self._names.append(name)
        self._plugins[name] = replacement

    def unload(self, name):
        self._names.remove(name)
        del self._plugins[name]

class Bot(object):
    __slots__ = ['server', 'server_name', 'address', 'nick', 'name', 'usermode',
                 'in_encodings', 'out_encoding', 'plugins', 'reason',
                 'exc_info', 'timeouts']

    def __init__(self, address):
        self.server = None
        self.server_name = None
        self.address = address
        self.nick = u'flexo'
        self.name = u'Flexo'
        self.usermode = u'-sw'
        self.timeouts = 0

        self.in_encodings = 'iso-8859-1', 'utf-8'
        self.out_encoding = 'iso-8859-1'

        self.reason = None
        self.exc_info = None

        self.plugins = Plugins(self)

    def run(self):
        while True:
            try:
                if not self.server:
                    self.connect()
                self.interact()

            except (socket.error, EnvironmentError):
                log.exception('Network error')

            if self.reason:
                if self.reason <> 'graceful':
                    self.disconnect()
                break

            time.sleep(reconnect_delay)

    def disconnect(self):
        log.info('Closing connection to server')
        try:
            self.server.close()
        except:
            log.exception('Error closing socket')
        self.server = None

        for plugin in self.plugins:
            plugin.on_disconnected()

    def quit(self, reason):
        self.reason = 'quit'
        self.send(u'QUIT :' + reason)

    def graceful(self):
        self.reason = 'graceful'
        self.send(u'PING ' + self.server_name)

    def initialize(self):
        for line in self.open_state('plugins'):
            self.plugins.load(line.strip())

    def reinitialize(self, other):
        if not other:
            self.reason = None
            return
            
        for key in other.__slots__:
            setattr(self, key, getattr(other, key))

        self.reason = None

        plugins = list(self.plugins)
        self.plugins = Plugins(self)
        for plugin in plugins:
            self.plugins.load(plugin.name)

    def connect(self):
        assert not self.server

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(self.address)
        self.server = s.makefile('rw')
        self.server_name = self.address[0]

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
        self.server._sock.settimeout(timeout)

        while not self.reason:
            try:
                line = self.server.readline()
                self.timeouts = 0
            except socket.timeout:
                self.timeouts = self.timeouts + 1
                if self.timeouts == max_timeouts:
                    log.warning('Connection timed out')
                    self.disconnect()
                    break
                self.send(u'PING ' + self.server_name)
                continue

            if line == '':
                if not self.reason:
                    log.warning('Lost connection')
                    self.disconnect()
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
        if message.command == '001':
            self.server_name = message.sender
        for plugin in self.plugins:
            if plugin.handle(message):
                break

    def network_log(self, txt):
        file = open('network.log', 'a')
        file.write('[%s] %s\n' % (time.asctime(), txt.encode('utf-8')))
        file.close()

    def open_state(self, name, mode='r'):
        return open('state/' + name, mode)

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

        self.channel = self.bot.plugins.channels.get(rest[0])
        self.tail = rest[-1]

    def reply(self, what):
        if self.channel:
            where = self.channel.name
        else:
            where = self.nick

        if what.startswith('<action> '):
            what = u'\x01ACTION %s\x01' % what[9:]
        elif what.startswith('<reply> '):
            what = what.split(' ', 1)[1]
        elif self.channel and self.nick:
            what = u'%s, %s' % (self.nick, what)

        self.bot.send(u'PRIVMSG %s :%s' % (where, what))
