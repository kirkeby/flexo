# vim:encoding=utf-8:

from flexo.plugin import Plugin

import random

class Random(Plugin):
    def on_bang_random(self, message, text):
        try:
            if '..' in text:
                a, b = map(int, text.split('..', 1))
            else:
                a, b = 1, int(text)
        except ValueError:
            return
        if not a < b:
            a, b = b, a

        message.reply(u'<action> kaster 1D%d' % (1 + b - a))
        message.reply(u'Terningen siger %d' % random.randint(a, b))

    def on_bang_choice(self, message, text):
        choices = text.split()
        message.reply(u'<action> trækker en lap papir fra hatten')
        message.reply(u'Valget faldt på %s' % random.choice(choices))

plugin = Random
