import random

got_its = ['Yeeees, yes', 'Har det!', 'Oki', 'You speak wisely, sir']

class Core:
    def __init__(self, bot):
        self.bot = bot
        self.bot.core = self

    def handle(self, sender, command, rest):
        return

    def reply(self, sender, where, txt):
        who = sender.split('!', 1)[0][1:]
        if where == self.bot.nick:
            self.bot.send('PRIVMSG %s :%s' % (who, txt))
        else:
            self.bot.send('PRIVMSG %s :%s, %s' % (where, who, txt))
        
    def got_it(self, who, where):
        txt = random.choice(got_its)
        self.reply(who, where, txt)

    def action(self, where, what):
        self.bot.send('PRIVMSG %s :\x01ACTION %s\x01' % (where, what))

plugin = Core
