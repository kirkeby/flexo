class Plugin:
    def __init__(self, bot):
        self.bot = bot

    def handle(self, sender, command, rest):
        if command == '001':
            self.on_connected()
        elif command == 'PRIVMSG':
            where, says = rest.split(':', 1)
            where = where.strip()

            if where == self.bot.nick:
                return self.on_private_msg(sender, says)
            else:
                return self.on_public_msg(sender, where, says)

    def on_connected(self):
        pass
    def on_private_msg(self, sender, says):
        pass
    def on_public_msg(self, sender, where, says):
        pass
