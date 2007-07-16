from flexo.plugin import Plugin
import traceback

class Remote(Plugin):
    def on_private_msg(self, sender, says):
        if not self.bot.core.is_oper(sender):
            return

        pieces = says.split(None, 1)
        cmd = pieces[0]
        if len(pieces) > 1:
            rest = pieces[1]
        else:
            rest = ''

        if cmd == 'eval':
            ctx = {
                'bot': self.bot,
            }
            try:
                result = eval(rest, ctx)
                if not result is None:
                    text = repr(result)
                    if len(text) > 60:
                        text = text[:60] + ' [..]'
                    self.bot.core.privmsg(sender, text)
            except Exception, e:
                self.bot.core.privmsg(sender, 'Failed: %r' % e)
                traceback.print_exc()
            return True

        elif cmd == 'load':
            try:
                replacement = self.load(rest)
            except Exception, e:
                self.bot.core.privmsg(sender, 'Failed: %r' % e)
                return True
                
            for i, plugin in enumerate(self.bot.plugins):
                if plugin.__class__.__name__ == replacement.__class__.__name__:
                    self.bot.plugins[i] = replacement
                    self.bot.core.privmsg(sender, 'Reloaded.')
                    break
            else:
                self.bot.plugins.append(replacement)
                self.bot.core.privmsg(sender, 'Loaded.')

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
