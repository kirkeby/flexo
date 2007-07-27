# vim:encoding=utf-8:

from flexo.plugin import Plugin
from flexo.prelude import is_it_friday

import random

class BeatMe(Plugin):
    def on_cmd_beatme(self, context, why):
        if not isinstance(context, tuple):
            return
        sender, channel = context
        
        if not self.bot.nick in self.bot.channels[channel]['opers']:
            txt = 'Braaaaaaaaaaaaains... Eh.. Mener, mangler +o'
            self.bot.core.reply(sender, channel, txt)
            return

        if not is_it_friday():
            who = self.bot.core.get_nick(sender)
            self.bot.send('KICK %s %s :*Kun* på en fredag!' % (channel, who))
            return

        if not why:
            why = 'Uuuuuuuuuuuht af min butik!'

        victims = [name for name in self.bot.channels[channel]['users']
                   if not name == self.bot.nick]
        who = random.choice(victims)

        self.bot.send('KICK %s %s :%s' % (channel, who, why))

plugin = BeatMe
