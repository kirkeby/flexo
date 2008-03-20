from flexo.plugin import Plugin

class Core(Plugin):
    def handle(self, message):
        if message.command == u'001':
            self.bot.server_name = message.prefix
        elif message.command == u'PING' and len(message.rest) == 1:
            self.bot.send(u'PONG :' + message.rest[0])

plugin = Core
