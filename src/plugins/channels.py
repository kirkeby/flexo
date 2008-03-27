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

    def on_welcome(self, message):
        self.channels = {}
        for line in self.bot.open_state('channels'):
            self.join(line.strip())

    def on_mode(self, message):
        if message.mode == '-o':
            for who in message.what.split():
                message.channel.on_deop(who)
        elif message.mode == '+o':
            for who in message.what.split():
                message.channel.on_op(who)

    def on_namreply(self, message):
        for nick in message.names.split():
            if nick[0] in '@+':
                flag, nick = nick[0], nick[1:]
            else:
                flag = ''

            message.channel.on_join(nick)
            if flag == '@':
                message.channel.on_op(nick)

    def on_join(self, message):
        message.channel.on_join(message.nick)
    def on_part(self, message):
        message.channel.on_part(message.nick)
    def on_kick(self, message):
        if message.target == self.bot.nick:
            self.bot.send(u'PRIVMSG %s :Grrr. . .' % message.nick)
            del self.channels[message.channel.name]
        else:
            message.channel.on_part(message.target)
    def on_quit(self, message):
        message.channel.on_part(message.nick)

    def get(self, name):
        return self.channels.get(name)

class Channel:
    def __init__(self, name, users, opers):
        self.name = name
        self.users = users
        self.opers = opers

    def on_op(self, who):
        if not who in self.opers:
            self.opers.append(who)
    def on_deop(self, who):
        if who in self.opers:
            self.opers.remove(who)
    def on_join(self, who):
        if not who in self.users:
            self.users.append(who)
    def on_part(self, who):
        if who in self.users:
            self.users.remove(who)
        self.on_deop(who)

plugin = Channels
