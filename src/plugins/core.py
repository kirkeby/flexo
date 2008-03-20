from flexo.plugin import Plugin

class Core(Plugin):
    def on_myinfo(self, message):
        self.bot.server_name = message.servername
    def on_ping(self, message):
        self.bot.send(u'PONG :' + message.source)

plugin = Core
