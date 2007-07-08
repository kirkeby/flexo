import pickle
import random

factoids = pickle.load(open('factoids'))

class Factoid:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        sender = sender.split('!', 1)[0][1:]

        try:
            where, what = rest.split(' ', 1)
        except:
            return

        if what.startswith(':!?'):
            facts = factoids.get(what[3:].strip(), None)
            if facts is None:
                self.bot.send('PRIVMSG %s :%s, Huh?!' % (where, sender))
            else:
                text = random.choice(facts)
                if text.startswith('<reply> '):
                    self.bot.send('PRIVMSG %s :%s' % (where, text[8:]))
                else:
                    self.bot.send('PRIVMSG %s :Jeg mener helt bestemt at %s er %s' % (where, what, text))
            return True

        elif what.startswith(':!!'):
            if not ' is ' in what:
                self.bot.send('PRIVMSG %s :%s, "!!dims is noget om dims" FAT DET!' % (where, sender))
                return True

            thing, text = what.split(' is ')
            thing = thing[3:]
            if thing in factoids:
                text.append(factoids[thing])
            else:
                factoids[thing] = [text]
            pickle.dump(factoids, open('factoids', 'w'))
            self.bot.send('PRIVMSG %s :%s, Yeeeeees, yes.' % (where, sender))
            return True

plugin = Factoid
