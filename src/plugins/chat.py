# -*- encoding: utf-8 -*-

from flexo.plugin import Plugin

class Chatter(Plugin):
    def on_privmsg(self, message):
        what = message.says

        if what.startswith(self.bot.nick.lower() + ', '):
            message.reply(u'NOBODY CARES!')
            return True
        elif what.startswith(self.bot.nick.lower() + ': '):
            message.reply(u'NOBODY CARES!')
            return True

plugin = Chatter
