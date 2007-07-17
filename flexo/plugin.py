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
        if not says.startswith('!'):
            return

        pieces = says.split(None, 1)
        if len(pieces) == 1:
            pieces.append('')

        cmd = pieces[0][1:]
        return self.on_public_cmd(sender, where, cmd, pieces[1])
    def on_public_cmd(self, sender, where, cmd, rest):
        handler = getattr(self, 'on_cmd_' + cmd, None)
        if not handler:
            return
        handler(sender, where, pieces[1])
        return True
