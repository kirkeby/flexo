# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_element

class GreetUser(Plugin):
    def on_join(self, channel, nick):
        greet = random_element([ g.split(' ', 1)[1]
                                 for g in open('greetings')
                                 if g.startswith(nick + ' ') ])
        if not greet:
            return

        if greet.startswith('<action> '):
            self.bot.core.action(channel, greet[9:])
        else:
            self.bot.send('PRIVMSG %s :%s' % (channel, greet))

    def on_cmd_newgreet(self, context, rest):
        if not ' ' in rest:
            self.reply(context, 'Syntaksen er: !newgreet <nick> <besked>')
            return

        open('greetings', 'a').write(rest + '\n')
        self.reply(context, "'tis done.")

plugin = GreetUser
