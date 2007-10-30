from flexo.prelude import *

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
        elif command == 'JOIN':
            channel = rest[1:]
            nick = sender.split('!')[0][1:]
            self.on_join(channel, nick)

    def on_connected(self):
        pass

    def on_private_msg(self, sender, says):
        if not says.startswith('!'):
            return

        pieces = says.split(None, 1)
        if len(pieces) == 1:
            pieces.append('')

        cmd = pieces[0][1:]
        
        if pieces[1].startswith('#'):
            pieces = pieces[1].split(None, 1)
            if len(pieces) == 1:
                pieces.append('')

            if not pieces[0] in self.bot.channels:
                text = 'Den kanal er jeg ikke med i.'
                self.bot.core.privmsg(sender, text)
                return
                
            return self.on_public_cmd(sender, pieces[0], cmd, pieces[1])

        else:
            return self.on_private_cmd(sender, cmd, pieces[1])

    def on_public_msg(self, sender, where, says):
        if not says.startswith('!'):
            return

        pieces = says.split(None, 1)
        if len(pieces) == 1:
            pieces.append('')

        cmd = pieces[0][1:]
        return self.on_public_cmd(sender, where, cmd, pieces[1])

    def on_join(self, channel, nick):
        pass

    def on_public_cmd(self, sender, where, cmd, rest):
        return self.on_cmd((sender, where), cmd, rest)
    def on_private_cmd(self, sender, cmd, rest):
        return self.on_cmd(sender, cmd, rest)
    def on_cmd(self, context, cmd, rest):
        handler = getattr(self, 'on_cmd_' + cmd, None)
        if not handler:
            return
        handler(context, rest)
        return True

    # FIXME - skal afprøves offline!
    #def is_oper(self, sender):
    #    return sender in [line.strip() for line in open('opers')]
    def reply(self, context, what):
        nick, channel = get_nick_channel(context)
        if channel:
            self.bot.send('PRIVMSG %s :%s, %s' % (channel, nick, what))
        else:
            self.bot.send('PRIVMSG %s :%s' % (nick, what))
