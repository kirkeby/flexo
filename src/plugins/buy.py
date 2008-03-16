# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import get_nick_channel

class Buy(Plugin):
    def on_cmd_buy(self, message, rest):
        if not message.channel:
            return

        if ' ' in rest:
            who, what = rest.split(' ', 1)
            action = u'<action> giver %s %s fra %s' % (who, what, message.nick)
        else:
            action = u'<action> installerer et clue-level i %s' % message.nick
        message.reply(action)

        return True

plugin = Buy
