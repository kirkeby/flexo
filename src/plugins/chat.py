# -*- encoding: utf-8 -*-

import re
from flexo.plugin import Plugin

class Chatter(Plugin):
    def on_privmsg(self, message):
        what = message.says

        if what.startswith(self.bot.nick.lower() + ', '):
            pass
        elif what.startswith(self.bot.nick.lower() + ': '):
            pass
        else:
            return False

        if re.search(r'\bbender\b', what, re.I):
            message.reply(u'Tell him I hate him!')
        else:
            message.reply(u'NOBODY CARES!')
        return True

plugin = Chatter
