from flexo import _eliza
import re

class Eliza:
    def __init__(self, bot):
        self.bot = bot
        self.therapist = _eliza.eliza()
        self.prefix = re.compile('%s[,:] ' % self.bot.nick, re.I)

    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        try:
            where, what = rest.split(' ', 1)
            what = what[1:]
        except:
            return
        m = self.prefix.match(what)
        if not m:
            return

        reply = self.therapist.respond(what[len(m.group(0)):])
        self.bot.core.reply(sender, where, reply)
        return True

plugin = Eliza
