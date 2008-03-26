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
    def __init__(self, bot, what='praise', path='praises'):
        Plugin.__init__(self, bot)

        self.what = what
        self.path = path

        setattr(self, 'on_bang_' + what, self._on_praise)
        setattr(self, 'on_bang_new' + what, self._on_newpraise)

    def _on_praise(self, message, rest):
        praiser = message.nick

        if rest.lower() == self.bot.nick.lower():
            self._on_self_praise(message)
            return True

        who = replace_pronouns(rest, praiser)
        template = random_line(self.bot.open_state(self.path))
        praise = template.replace('%s', who)
        message.reply(u'<action>' + praise)

    def _on_newpraise(self, message, rest):
        if not '%s' in rest:
            message.reply(u'Halllo. Der skal være %%s i en %s!' % self.what)
        else:
            file = self.bot.open_state(self.path, 'a')
            file.write(rest.encode('utf-8') + '\n')
            file.close()
            message.reply(random.choice(got_its))

    def _on_self_praise(self, message):
        message.reply(u'<action> klapper sig selv på hovedet')

class Larter(Praiser):
    def __init__(self, bot):
        Praiser.__init__(self, bot, 'lart', 'larts')

    def _on_self_praise(self, message):
        praiser = message.nick
        where = message.channel.name
        message.reply(u'<action> losser %s så hårdt i bollerne at '
                             u'han ryger ud af %s' % (praiser, where))
        self.bot.send(u'KICK %s %s :Så kan du måske lære det!'
                      % (where, praiser))

class UltraLarter(Praiser):
    def __init__(self, bot):
        self.bot = bot
        self.what = 'ultralart'
        self.path = 'ultralarts'

    def _on_self_praise(self, message):
        praiser = message.nick
        where = message.channel.name
        action = u'<action> klynger %s op med en død rottes hale' % praiser
        message.reply(action)
        self.bot.send(u'KICK %s %s :Så kan du måske lære det!'
                      % (where, praiser))

class MetaPlugin(Plugin):
    def __init__(self, bot):
        self.plugins = Praiser(bot), Larter(bot), UltraLarter(bot)
    def handle(self, message):
        for plugin in self.plugins:
            if plugin.handle(message):
                return True
        return False

plugin = MetaPlugin
