from flexo.praise import Praiser

class Larter(Praiser):
    def __init__(self, bot):
        self.bot = bot
        self.what = 'lart'
        self.path = 'larts'

plugin = Larter
