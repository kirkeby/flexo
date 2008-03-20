# -*- encoding: utf-8 -*-
from __future__ import absolute_import

from flexo.protocol import is_channel
from flexo.protocol import parse_prefix
from flexo.protocol import parse_parameters

empty_parameters = { 'channel': None, 'reason': None, }

class Message:
    def __init__(self, bot, prefix, command, rest):
        self.bot = bot
        self.prefix = prefix
        if prefix:
            self.nick, self.userhost = parse_prefix(self.prefix)
        self.command = command

        self.rest = rest

        params = {}
        params.update(empty_parameters)
        params.update(parse_parameters(self.command, self.rest))
        params['channel'] = self.bot.plugins.channels.get(params['channel'])
        self.__dict__.update(params)

    def reply(self, what):
        if self.channel:
            where = self.channel.name
        else:
            where = self.nick

        if what.startswith('<action>'):
            what = u'\x01ACTION %s\x01' % what[8:].strip()
        elif what.startswith('<reply>'):
            what = what[7:].strip()
        elif self.channel and self.nick:
            what = u'%s, %s' % (self.nick, what)

        self.bot.send(u'PRIVMSG %s :%s' % (where, what))
