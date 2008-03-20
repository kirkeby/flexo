# -*- encoding: utf-8 -*-
from flexo.plugin import Plugin
from flexo.prelude import random_element

class GreetUser(Plugin):
    def on_join(self, message):
        nick = message.nick.encode('utf-8')
        greet = random_element([ g.split(' ', 1)[1].decode('utf-8')
                                 for g in self.bot.open_state('greetings')
                                 if g.startswith(nick + ' ') ])
        if not greet:
            return

        if greet.startswith(u'<action>'):
            greet = u'\x01ACTION %s\x01' % greet[8:].strip()
        self.bot.send(u'PRIVMSG %s :%s' % (message.channel, greet))

    def on_bang_newgreet(self, message, rest):
        if not ' ' in rest:
            message.reply(u'Syntaksen er: !newgreet <nick> <besked>')
            return

        file = self.bot.open_state('greetings', 'a')
        file.write(rest.encode('utf-8') + '\n')
        file.close()
        message.reply(u'Det skal jeg huske!')

plugin = GreetUser
