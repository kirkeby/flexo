# vim:encoding=utf-8:

from flexo.plugin import Plugin
from flexo.prelude import is_it_friday
from flexo.prelude import is_bot

import random

class BeatMe(Plugin):
    def on_bang_beatme(self, message, why):
        if not message.channel:
            return
        
        if not self.bot.nick in message.channel.opers:
            message.reply(u'Braaaaaaaaaaaaains... Eh.. Mener, mangler +o')
            return

        if not is_it_friday():
            self.bot.send(u'KICK %s %s :*Kun* på en fredag!'
                          % (message.channel.name, message.nick))
            return

        if not why:
            why = 'Uuuuuuuuuuuht af min butik!'

        victims = [name for name in message.channel.users
                   if not name == self.bot.nick and not is_bot(name)]
        if not victims:
            return
        who = random.choice(victims)

        self.bot.send(u'KICK %s %s :%s' % (message.channel.name, who, why))

plugin = BeatMe
