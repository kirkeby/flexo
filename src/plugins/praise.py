# vim:encoding=utf-8

import re
import random

from flexo.plugin import Plugin
from flexo.prelude import got_its
from flexo.prelude import random_line

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

    def on_public_cmd(self, message, cmd, rest):
        praiser = message.nick
        if cmd == self.what:
            if rest.lower() == self.bot.nick.lower():
                self.on_self_praise(message)
                return True

            who = replace_pronouns(rest, praiser)
            template = random_line(self.bot.open_state(self.path))
            praise = template.replace('%s', who)
            message.reply_action(praise)

            return True

        elif cmd == 'new' + self.what:
            if not '%s' in rest:
                message.reply(u'Halllo. Der skal være %%s i en %s!' % self.what)
            else:
                self.bot.open_state(self.path, 'a').write(rest.encode('utf-8') + '\n')
                message.reply(random.choice(got_its))
            return True

    def on_self_praise(self, message):
        message.reply_action(u'klapper sig selv på hovedet')

class Larter(Praiser):
    def __init__(self, bot):
        self.bot = bot
        self.what = 'lart'
        self.path = 'larts'

    def on_self_praise(self, message):
        message.reply_action(u'losser %s så hårdt i bollerne at '
                             u'han ryger ud af %s' % (praiser, where))
        self.bot.send(u'KICK %s %s :Så kan du måske lære det!'
                      % (message.channel.name, message.nick))

class MetaPlugin:
    def __init__(self, bot):
        self.plugins = Praiser(bot), Larter(bot)
    def handle(self, message):
        for plugin in self.plugins:
            if plugin.handle(message):
                return True
        return False
    def get_state(self):
        return tuple(p.get_state() for p in self.plugins)
    def set_state(self, states):
        for p, state in zip(self.plugins, states):
            p.set_state(state)

plugin = MetaPlugin
