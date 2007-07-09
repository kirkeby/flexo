import pickle
import random

factoids = pickle.load(open('factoids'))

class Factoid:
    def __init__(self, bot):
        self.bot = bot
    def handle(self, sender, command, rest):
        if not command == 'PRIVMSG':
            return

        try:
            where, what = rest.split(' ', 1)
        except:
            return

        if what.startswith(':!?'):
            what = what[3:].strip()
            facts = factoids.get(what, None)
            if facts is None:
                self.bot.core.reply(sender, where, 'Huh?!')
            else:
                text = random.choice(facts)
                if text.startswith('<reply> '):
                    self.bot.send('PRIVMSG %s :%s' % (where, text[8:]))
                else:
                    txt = 'Jeg mener helt bestemt at %s er %s' % (what, text)
                    self.bot.core.reply(sender, where, txt)
            return True

        elif what.startswith(':!!'):
            if not ' is ' in what:
                txt = '"!!dims is noget om dims" <- FAT DET!'
                self.bot.core.reply(sender, where, txt)
                return True

            thing, text = what.split(' is ')
            thing = thing[3:].strip()
            if thing in factoids:
                factoids[thing].append(text)
            else:
                factoids[thing] = [text]
            pickle.dump(factoids, open('factoids', 'w'))
            self.bot.core.got_it(sender, where)
            return True

        elif what.startswith(':!listfacts '):
            prefix = what.split(' ', 1)[1].strip()
            facts = []
            for key in factoids:
                if key.startswith(prefix):
                    facts.append(key)

            if facts:
                reply = 'Jeg ved ting om ' + ', '.join(facts)
            else:
                reply = 'No clue'
            self.bot.core.reply(sender, where, reply)
            return True

plugin = Factoid
