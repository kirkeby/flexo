class Channels:
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(self.bot, 'channels'):
            self.bot.channels = {}

    def handle(self, sender, command, rest):
        if command == 'MODE':
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

            return True

    def get_channel(self, name):
        if not name in self.bot.channels:
            self.bot.channels[name] = {
                'opers': [],
            }
        return self.bot.channels[name]

plugin = Channels
