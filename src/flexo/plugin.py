# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from flexo.prelude import is_bot
from flexo.protocol import numerical_names

class Plugin:
    def __init__(self, bot):
        self.bot = bot

    def get_state(self):
        return None
    def set_state(self, state):
        pass

    def handle(self, message):
        if message.command == u'PRIVMSG' and is_bot(message.nick):
            return True

        command_name = numerical_names.get(message.command, message.command)
        handler = getattr(self, u'on_' + command_name.lower(), None)
        if handler:
            return handler(message)

    def on_privmsg(self, message):
        if not message.says.startswith('!'):
            return

        pieces = message.says.split(None, 1)
        pieces.append(u'')
        cmd, rest = pieces[:2]

        handler = getattr(self, 'on_bang_' + cmd[1:], None)
        if not handler:
            return
        handler(message, rest)
        return True
