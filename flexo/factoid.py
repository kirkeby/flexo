import re
import pickle
import random

from flexo.plugin import Plugin

factoids = pickle.load(open('factoids'))

define_re = re.compile(r'^!!\s*(.*)\s+(is|er)\s+(.*)$', re.I)
huh = ['Huh?!', 'I know not this %s you speak of',
       'Aner det ikke', 'Kein ahnung']

class Factoid(Plugin):
    def on_public_msg(self, sender, where, what):
        if what.startswith('!?'):
            what = what[2:].strip()
            self.on_lookup(sender, where, what)
            return True

        elif what.startswith('!!'):
            self.on_define(sender, where, what)
            return True

        elif what.startswith('!listfacts '):
            prefix = what.split(' ', 1)[1].strip()
            self.on_list(sender, where, prefix.lower())
            return True

    def on_lookup(self, sender, where, what):
        facts = factoids.get(what, None)
        if facts is None:
            reply = random.choice(huh).replace('%s', what)
            self.bot.core.reply(sender, where, reply)

        else:
            text = random.choice(facts)
            if text.startswith('<reply> '):
                self.bot.send('PRIVMSG %s :%s' % (where, text[8:]))
            elif text.startswith('<action> '):
                self.bot.core.action(where, text[9:])
            else:
                txt = 'Jeg mener helt bestemt at %s er %s' % (what, text)
                self.bot.core.reply(sender, where, txt)
        
    def on_define(self, sender, where, what):
        m = define_re.match(what)
        if not m:
            txt = '"!!dims is noget om dims" <- FAT DET!'
            self.bot.core.reply(sender, where, txt)
            return True

        thing, how, text = m.groups()
        if thing in factoids:
            factoids[thing].append(text)
        else:
            factoids[thing] = [text]
        pickle.dump(factoids, open('factoids', 'w'))
        self.bot.core.got_it(sender, where)

    def on_list(self, sender, where, prefix):
        facts = []
        for key in factoids:
            if key.lower().startswith(prefix):
                facts.append(key)

        if facts:
            reply = 'Jeg ved ting om ' + ', '.join(facts)
        else:
            reply = 'No clue'
        self.bot.core.reply(sender, where, reply)

plugin = Factoid
