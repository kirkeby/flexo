# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_element

class Excuse(Plugin):
    def on_cmd_excuse(self, sender, channel, why):
        self.bot.core.reply(sender, channel, random_element(open('excuses')))

plugin = Excuse
