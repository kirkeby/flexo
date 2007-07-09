# vim:encoding=utf-8

import random

class Praiser:
    def __init__(self, bot):
        self.bot = bot
        self.what = 'praise'
        self.path = 'praises'
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        praiseer = sender.split('!', 1)[0]

        try:
            where, what, who = rest.split(' ', 2)
        except:
            return

        if what == (':!' + self.what):
            praises = open(self.path).readlines()
            praise = random.choice(praises).strip() % who

            self.bot.core.action(where, praise)

            return True

        if what == (':!new' + self.what):
            if not '%s' in who:
                self.bot.core.reply(where, praiseer,
                                    u'Halllo. Der skal være %%s i en %s!'
                                    % self.what)
            else:
                open(self.path, 'a').write(who + '\n')
            return True

plugin = Praiser
