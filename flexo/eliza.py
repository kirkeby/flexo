# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo import _eliza
import re

class Eliza(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.therapist = _eliza.eliza()
        self.prefix = re.compile('%s[,:] ' % self.bot.nick, re.I)

    def on_public_msg(self, sender, channel, what):
        m = self.prefix.match(what)
        if not m:
            return

        reply = self.therapist.respond(what[len(m.group(0)):])
        self.bot.core.reply(sender, where, reply)
        return True

plugin = Eliza
