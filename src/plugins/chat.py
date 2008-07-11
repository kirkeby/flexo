# -*- encoding: utf-8 -*-

import re
from flexo.plugin import Plugin

def compile(line):
    pattern, reply = line.strip().split(' -> ', 1)
    return pattern.strip(), reply.strip()
replies = [ compile(line.decode('utf-8')) for line in open('state/chat') ]

class Chatter(Plugin):
    def on_privmsg(self, message):
        what = message.says

        nick_pattern = self.bot.nick + '[,:]\\s*'
        for pattern, reply in replies:
            pattern = pattern.replace('<nick>', nick_pattern)
            if re.match(pattern, what, re.I):
                break
        else:
            return False

        message.reply(reply)
        return True

plugin = Chatter
