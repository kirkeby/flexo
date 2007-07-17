# vim:encoding=utf-8

from flexo.plugin import Plugin
import random

class Praiser(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.what = 'praise'
        self.path = 'praises'

    def on_public_cmd(self, sender, where, cmd, rest):
        if cmd == self.what:
            praises = open(self.path).readlines()
            praise = random.choice(praises).strip().replace('%s', rest)
            self.bot.core.action(where, praise)
            return True

        elif cmd == 'new' + self.what:
            if not '%s' in rest:
                self.bot.core.reply(sender, where,
                                    u'Halllo. Der skal være %%s i en %s!'
                                    % self.what)
            else:
                open(self.path, 'a').write(rest + '\n')
                self.bot.core.got_it(sender, where)
            return True

plugin = Praiser
