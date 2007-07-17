from flexo.plugin import Plugin

class Buy(Plugin):
    def on_cmd_buy(self, sender, where, rest):
        buyer = sender.split('!')[0][1:]
        if ' ' in rest:
            who, what = rest.split(' ', 1)
            action = 'giver %s %s fra %s' % (who, what, buyer)
            self.bot.core.action(where, action)
        else:
            action = 'installerer et clue-level i %s' % buyer
            self.bot.core.action(where, action)

        return True

    def on_private_cmd(self, sender, cmd, rest):
        if cmd == 'buy':
            try:
                where, who, rest = rest.split(' ', 2)
            except ValueError:
                text = '"!buy #channel someone something"'
                self.bot.core.privmsg(sender, text)
                return True

            if not where in self.bot.channels:
                text = 'Den kanal er jeg ikke med i.'
                self.bot.core.privmsg(sender, text)
            else:
                self.on_cmd_buy(sender, where, who + ' ' + rest)

            return True

plugin = Buy
