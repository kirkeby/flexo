# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_line

class Excuse(Plugin):
    def on_cmd_excuse(self, message, why):
        message.reply(random_line('excuses'))

plugin = Excuse
