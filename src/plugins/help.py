# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_line
class Help(Plugin):
    def on_bang_help(self, message, rest):
        message.reply(random_line(self.bot.open_state('help')))
plugin = Help
