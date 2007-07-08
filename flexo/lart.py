import random

class Larter:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        larter = sender.split('!', 1)[0][1:]
        try:
            where, what, who = rest.split(' ', 2)
        except:
            return

        if what == ':!lart':
            if who == self.bot.nick:
                who = larter

            larts = open('larts').readlines()
            lart = random.choice(larts).strip() % who

            self.bot.send('PRIVMSG %s :\x01ACTION %s\x01' % (where, lart))

            return True

        if what == ':!newlart':
            if not '%s' in who:
                self.bot.send('PRIVMSG %s :%s, Stoopid. Der skal være %%s i en lart!'
                              % (where, larter))
            else:
                open('larts', 'a').write(who + '\n')
                self.bot.send('PRIVMSG %s :%s, Har det!'
                              % (where, larter))
            return True

plugin = Larter
