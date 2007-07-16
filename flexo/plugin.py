class Plugin:
    def __init__(self, bot):
        self.bot = bot

    def handle(self, sender, command, rest):
        if command == '001':
            self.connected()

    def connected(self):
        pass
