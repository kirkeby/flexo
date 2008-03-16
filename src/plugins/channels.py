# -*- encoding: utf-8 -*-

from flexo.plugin import Plugin

class Channels(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        self.channels = {}

    def get_state(self):
        return [ (c.name, c.users, c.opers) for c in self.channels.values() ]
    def set_state(self, triplets):
        for name, users, opers in triplets:
            self.channels[name] = Channel(name, users, opers)

    def join(self, name):
        if name in self.channels:
            raise ValueError('Already in %s' % name)
        self.channels[name] = Channel(name, [], [])
        self.bot.send(u'JOIN %s' % name)
        self.save_channels()
    def part(self, name):
        del self.channels[name]
        self.bot.send(u'PART %s :Så længe sugere!' % name)
        self.save_channels()

    def save_channels(self):
        file = self.bot.open_state('channels', 'w')
        for name in self.channels.keys():
            file.write(name + '\n')
        file.close()

    def on_connected(self):
        for line in self.bot.open_state('channels'):
            self.join(line.strip())
    def on_disconnected(self):
        self.channels = {}

    def handle(self, message):
        if Plugin.handle(self, message):
            return True

        if message.channel and message.command == 'MODE':
            name, mode, who = message.rest
            who = who.split()

            if mode == '-o':
                for someone in who:
                    if someone in message.channel.opers:
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
        if channel:
            channel.users.remove(nick)
            if nick in channel.opers:
                channel.opers.remove(nick)

    def get(self, name):
        return self.channels.get(name)

class Channel:
    def __init__(self, name, users, opers):
        self.name = name
        self.users = users
        self.opers = opers

plugin = Channels
