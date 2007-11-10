# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo import _eliza
import re

class Eliza(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.therapist = _eliza.eliza()

    def on_public_msg(self, message): 
        what = message.tail
        prefix = re.compile('%s[,:] ' % self.bot.nick, re.I)
        m = prefix.match(what)
        if not m:
            return

        reply = self.therapist.respond(what[len(m.group(0)):])
        message.reply(reply)
        return True

plugin = Eliza
