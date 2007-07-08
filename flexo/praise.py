import random

class Praiser:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        praiseer = sender.split('!', 1)[0]

        try:
            where, what, who = rest.split(' ', 2)
        except:
            return

        if what == ':!praise':
            praises = open('praises').readlines()
            praise = random.choice(praises).strip() % who

            self.bot.send('PRIVMSG %s :\x01ACTION %s\x01' % (where, praise))

            return True

        if what == ':!newpraise':
            if not '%s' in who:
                self.bot.send('PRIVMSG %s :%s, Halllo. Der skal være %%s i en praise!'
                              % (where, praiseer))
            else:
                open('praises', 'a').write(who + '\n')
            return True

plugin = Praiser
