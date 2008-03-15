# -*- encoding: utf-8 -*-

from flexo.plugin import Plugin
from flexo.prelude import is_oper

class Channels(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.channels = {}

    def get_state(self):
        return [ (c.name, c.users, c.opers) for c in self.channels.values() ]
    def set_state(self, triplets):
        for name, users, opers in triplets:
            self.channels[name] = Channel(name, users, opers)

    def on_connected(self):
        for line in open('channels'):
            name = line.strip()
            self.channels[name] = Channel(name, [], []) 
            self.bot.send(u'JOIN %s' % name)

    def handle(self, message):
        if Plugin.handle(self, message):
            return True

        if message.channel and message.command == 'MODE':
            name, mode, who = message.rest
            who = who.split()

            if mode == '-o':
                for someone in who:
                    if someone in channel.opers:
                        message.channel.opers.remove(someone)
            elif mode == '+o':
                for someone in who:
                    message.channel.opers.append(someone)

        elif message.command == '353':
            name = message.rest[2]
            channel = self.get(name)

            for user in message.tail.split():
                if user[0] == '@':
                    user = user[1:]
                    if not user in channel.opers:
                        channel.opers.append(user)
                if user[0] == '+':
                    user = user[1:]
                if not user in channel.users:
                    channel.users.append(user)

    def on_join(self, name, nick):
        channel = self.get(name)
        if channel:
            channel.users.append(nick)

    def on_part(self, name, nick, reason):
        channel = self.get(name)
        if channel and nick == self.bot.nick:
            del self.channels[name]

        elif channel:
            channel.users.remove(nick)
            if nick in channel.opers:
                channel.opers.remove(nick)

    def get(self, name):
        return self.channels.get(name)

    def on_cmd_join(self, message, name):
        if not is_oper(message.sender):
            return

        if name in self.channels:
            message.reply('Der er jeg allerede!')
            return

        self.channels[name] = Channel(name, [], []) 
        self.bot.send('JOIN ' + name)
        message.reply('Oki.')

    def on_cmd_part(self, message, name):
        if not is_oper(message.sender):
            return

        if not name and message.channel:
            name = message.channel.name
        if not name in self.channels:
            message.reply('Der er jeg ikke!')
            return

        message.reply('Jeg fordufter.')
        self.bot.send('PART %s :%s fik mig til det!' % (name, message.nick))

class Channel:
    def __init__(self, name, users, opers):
        self.name = name
        self.users = users
        self.opers = opers

plugin = Channels
