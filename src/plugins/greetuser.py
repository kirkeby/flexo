# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_element

class GreetUser(Plugin):
    def on_join(self, channel, nick):
        nick = nick.encode('utf-8')
        greet = random_element([ g.split(' ', 1)[1]
                                 for g in self.bot.open_state('greetings')
                                 if g.startswith(nick + ' ') ])
        if not greet:
            return

        greet = greet.decode('utf-8')
        if greet.startswith('<action> '):
            message.reply_action(greet[9:])
        else:
            self.bot.send('PRIVMSG %s :%s' % (message.channel.name, greet))

    def on_cmd_newgreet(self, message, rest):
        if not ' ' in rest:
            message.reply(u'Syntaksen er: !newgreet <nick> <besked>')
            return

        self.bot.open_state('greetings', 'a').write(rest.encode('utf-8') + '\n')
        message.reply(u'Det skal jeg huske!')

plugin = GreetUser
