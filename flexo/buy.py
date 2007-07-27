from flexo.plugin import Plugin

class Buy(Plugin):
    def on_cmd_buy(self, context, rest):
        if not isinstance(context, tuple):
            return

        sender, channel = context
        buyer = sender.split('!')[0][1:]

        if ' ' in rest:
            who, what = rest.split(' ', 1)
            action = 'giver %s %s fra %s' % (who, what, buyer)
            self.bot.core.action(channel, action)
        else:
            action = 'installerer et clue-level i %s' % buyer
            self.bot.core.action(channel, action)

        return True

plugin = Buy
