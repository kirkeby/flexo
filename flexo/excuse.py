from flexo.plugin import Plugin
import random

def random_element(iter):
    '''Retrieve a random item from an iterable object of unknown length,
    looping through it just once.'''

    it = None
    for i, e in enumerate(iter):
        if random.uniform(0, i) < 1:
            it = e

    return it

class Excuse(Plugin):
    def on_cmd_excuse(self, sender, channel, why):
        self.bot.core.reply(sender, channel, random_element(open('excuses')))

plugin = Excuse
