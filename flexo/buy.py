# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import get_nick_channel

class Buy(Plugin):
    def on_cmd_buy(self, context, rest):
        if not isinstance(context, tuple):
            return

        buyer, channel = get_nick_channel(context)
        if not channel:
            return

        if ' ' in rest:
            who, what = rest.split(' ', 1)
            action = 'giver %s %s fra %s' % (who, what, buyer)
            self.bot.core.action(channel, action)
        else:
            action = 'installerer et clue-level i %s' % buyer
            self.bot.core.action(channel, action)

        return True

plugin = Buy
