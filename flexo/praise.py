# vim:encoding=utf-8

import re
import random

my_pronouns_re = re.compile(r'\b(mig|min|mine|mit)\b', re.I)
specials = {
    'mig': lambda nick: nick,
}

def replace_pronouns(text, who):
    start = 0
    while True:
        m = my_pronouns_re.search(text, start)
        if not m:
            break

        pronoun, = m.groups()
        if pronoun in specials:
            replacement = specials[pronoun](who)
        elif start == 0:
            if who.endswith('s'):
                replacement = who
            else:
                replacement = who + 's'
        else:
            replacement = 'hans'

        s, e = m.span()
        start = e
        text = text[:s] + replacement + text[e:]

    return text

class Praiser:
    def __init__(self, bot):
        self.bot = bot
        self.what = 'praise'
        self.path = 'praises'
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        praiseer = self.bot.core.get_nick(sender)
        try:
            where, what, who = rest.split(' ', 2)
        except:
            return

        if what == (':!' + self.what):
            praises = open(self.path).readlines()

            who = replace_pronouns(who, praiseer)
            praise = random.choice(praises).strip().replace('%s', who)

            self.bot.core.action(where, praise)

            return True

        if what == (':!new' + self.what):
            if not '%s' in who:
                self.bot.core.reply(where, praiseer,
                                    u'Halllo. Der skal være %%s i en %s!'
                                    % self.what)
            else:
                self.bot.core.got_it(praiseer, where)
                open(self.path, 'a').write(who + '\n')
            return True

plugin = Praiser
