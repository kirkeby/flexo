from flexo.plugin import Plugin

class Channels(Plugin):
    def __init__(self, bot):
        Plugin.__init__(self, bot)
        if not hasattr(self.bot, 'channels'):
            self.bot.channels = {}

        if self.bot.server:
            self.on_connected()

    def on_connected(self):
        for line in open('channels'):
            name = line.strip()
            if not name in self.bot.channels:
                self.bot.send('JOIN %s' % name)
            else:
                self.bot.send('NAMES %s' % name)

    def handle(self, sender, command, rest):
        if Plugin.handle(self, sender, command, rest):
            return True

        elif command == 'MODE':
            channel, mode, who = rest.split(' ', 2)
            who = who.split()
            ch = self.get_channel(channel)

            if mode == '-o':
                for someone in who:
                    if someone in ch['opers']:
                        ch['opers'].remove(someone)
            elif mode == '+o':
                for someone in who:
                    ch['opers'].append(someone)

        elif command == 'JOIN':
            channel = rest[1:]
            who = sender.split('!')[0][1:]
            self.bot.channels[channel]['users'].append(who)
        elif command == 'PART':
            channel = rest[1:]
            who = sender.split('!')[0][1:]
            self.bot.channels[channel]['users'].remove(who)
            if who in self.bot.channels[channel]['opers']:
                self.bot.channels[channel]['opers'].remove(who)

        elif command == '353':
            before, users = rest.split(':', 1)
            names = []
            opers = []
            for user in users.split():
                if user[0] == '@':
                    opers.append(user[1:])
                if user[0] == '@' or user[0] == '+':
                    user = user[1:]
                names.append(user)
            channel = before.split(' ')[2]
            ch = self.get_channel(channel)
            ch['users'] = names
            ch['opers'] = opers

    def get_channel(self, name):
        if not name in self.bot.channels:
            self.bot.channels[name] = {
                'opers': [],
                'users': [],
            }
        return self.bot.channels[name]

plugin = Channels
