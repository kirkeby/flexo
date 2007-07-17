from flexo.plugin import Plugin
import random

class BeatMe(Plugin):
    def on_cmd_beatme(self, sender, channel, why):
        if not self.bot.nick in self.bot.channels[channel]['opers']:
            txt = 'Braaaaaaaaaaaaains... Eh.. Mener, mangler +o'
            self.bot.core.reply(sender, channel, txt)

        if not why:
            who = 'Uuuuuuuuuuuht af min butik!'

        victims = [name for name in self.bot.channels[channel]['users']
                   if not name == self.bot.nick]
        who = random.choice(victims)
        self.bot.send('KICK %s %s :%s' % (channel, who, why))

plugin = BeatMe
