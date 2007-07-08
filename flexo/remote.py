class Remote:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if not sender == ':kirkeby!kirkeby@localhost.localdomain':
            return
        if not command == 'PRIVMSG':
            return

        try:
            where, cmd, rest = rest.split(' ', 2)
        except:
            return

        if cmd == ':eval':
            ctx = {
                'bot': self.bot,
            }
            try:
                result = eval(rest, ctx)
                if not result is None:
                    self.bot.send('PRIVMSG kirkeby :' + repr(result))
            except:
                self.bot.send('PRIVMSG kirkeby :Failed.')
                traceback.print_exc()
            return True

        elif cmd == ':load':
            try:
                self.bot.plugins.append(self.load(rest))
            except:
                self.bot.send('PRIVMSG kirkeby :Failed.')
                raise
            self.bot.send('PRIVMSG kirkeby :Loaded.')
            return True
        
        elif cmd == ':reload':
            try:
                replacement = self.load(rest)
            except:
                self.bot.send('PRIVMSG kirkeby :Failed.')
                raise
                
            self.bot.plugins.append(self.load(rest))
            for i, plugin in enumerate(self.bot.plugins):
                if plugin.__class__.__name__ == replacement.__class__.__name__:
                    self.bot.plugins[i] = replacement
                    self.bot.send('PRIVMSG kirkeby :Reloaded.')
                    break
            else:
                self.bot.send('PRIVMSG kirkeby :Not found.')

            return True

    def load(self, name):
        file = 'flexo/%s.py' % name
        code = compile(open(file).read(), file, 'exec')
        ctx = {}
        module = eval(code, ctx, ctx)
        klass = ctx['plugin']
        plugin = klass(self.bot)
        return plugin

plugin = Remote
