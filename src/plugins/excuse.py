# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_line

class Excuse(Plugin):
    def on_bang_excuse(self, message, why):
        message.reply(random_line(self.bot.open_state('excuses')))

plugin = Excuse
