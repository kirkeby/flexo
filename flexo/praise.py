# vim:encoding=utf-8

from flexo.plugin import Plugin
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

class Praiser(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.what = 'praise'
        self.path = 'praises'

    def on_public_cmd(self, sender, where, cmd, rest):
        praiser = self.bot.core.get_nick(sender)
        if cmd == self.what:
            praises = open(self.path).readlines()

            if rest == self.bot.nick:
                who = 'sig selv'
            else:
                who = replace_pronouns(rest, praiser)

            praise = random.choice(praises).strip().replace('%s', who)
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
