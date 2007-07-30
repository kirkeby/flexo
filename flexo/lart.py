# vim:encoding=utf-8:

from flexo.praise import Praiser

class Larter(Praiser):
    def __init__(self, bot):
        self.bot = bot
        self.what = 'lart'
        self.path = 'larts'

    def on_self_praise(self, where, praiser):
        self.bot.core.action(where, u'losser %s så hårdt i bollerne at han ryger ud af %s' % (praiser, where))
        self.bot.send(u'KICK %s %s :Så kan du måske lære det!'
                      % (where, praiser))

plugin = Larter
