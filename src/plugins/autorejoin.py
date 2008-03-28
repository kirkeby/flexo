# -*- encoding: utf-8 -*-

from flexo.plugin import Plugin

class Channels(Plugin):
    def on_kick(self, message):
        if message.target <> self.bot.nick:
            return

        self.bot.plugins.channels.join(message.channel.name)
        message.reply(u'<action> pudser et kobbel vilde ulve på %s'
                      % message.nick)

plugin = Channels
