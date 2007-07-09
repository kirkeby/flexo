import random

class BeatMe:
    def __init__(self, bot):
        self.bot = bot

    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        try:
            pieces = rest.split(' ', 2)
            if len(pieces) == 3:
                where, what, why = pieces
            else:
                where, what = pieces
                why = 'Why the hell not?!'
        except:
            return

        if not where in self.bot.channels:
            return

        if what == ':!beatme':
            if not self.bot.nick in self.bot.channels[where]['opers']:
                txt = 'Braaaaaaaaaaaaains... Eh.. Mener, mangler +o'
                self.bot.core.reply(sender, where, txt)
                return True

            victims = [name for name in self.bot.channels[where]['users']
                       if not name == self.bot.nick]
            who = random.choice(victims)
            self.bot.send('KICK %s %s :%s' % (where, who, why))
            return True

plugin = BeatMe
