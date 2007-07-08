class BeatMe:
    def __init__(self, bot):
        self.bot = bot

    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        beater = sender.split('!', 1)[0]
        try:
            where, what, who = rest.split(' ', 2)
        except:
            return

        if what == ':!beatme':
            if ' ' in who:
                who, why = who.split(' ', 1)
            else:
                why = 'Fordi!'

            if who == self.bot.nick:
                self.bot.send('KICK %s %s :Spejl!' % (where, beater))
            else:
                self.bot.send('KICK %s %s :%s' % (where, who, why))

            return True

plugin = BeatMe
