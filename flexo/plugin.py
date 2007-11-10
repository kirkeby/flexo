# -*- encoding: utf-8 -*-
class Plugin:
    def __init__(self, bot):
        self.bot = bot

    def get_state(self):
        return None
    def set_state(self, state):
        pass

    def handle(self, message):
        if message.command == u'001':
            self.on_connected()

        elif message.command == u'PRIVMSG':
            if message.channel and message.nick:
                return self.on_public_msg(message)
            elif message.nick:
                return self.on_private_msg(message)

        elif message.command == u'JOIN':
            self.on_join(message.channel.name, message.nick)

        elif message.command == u'PART':
            self.on_part(message.channel.name, message.nick, message.tail)

    def on_connected(self):
        pass

    def on_private_msg(self, message):
        says = message.rest[-1]
        if not says.startswith('!'):
            return

        pieces = says.split(None, 1)
        if len(pieces) == 1:
            pieces.append('')
        cmd = pieces[0][1:].encode('ascii', 'ignore')
        
        return self.on_private_cmd(message, cmd, pieces[1])

    def on_public_msg(self, message):
        says = message.tail
        if not says.startswith('!'):
            return

        pieces = says.split(None, 1)
        if len(pieces) == 1:
            pieces.append('')
        cmd = pieces[0][1:].encode('ascii', 'ignore')

        return self.on_public_cmd(message, cmd, pieces[1])

    def on_join(self, channel, nick):
        pass
    def on_part(self, channel, nick, reason):
        pass

    def on_public_cmd(self, message, cmd, rest):
        return self.on_cmd(message, cmd, rest)
    def on_private_cmd(self, message, cmd, rest):
        return self.on_cmd(message, cmd, rest)
    def on_cmd(self, message, cmd, rest):
        handler = getattr(self, 'on_cmd_' + cmd, None)
        if not handler:
            return
        handler(message, rest)
        return True
