import re
import random

from flexo.plugin import Plugin

define_format = r'^!!\s*(.*?)\s+(er|har)\s+(.*)$'
define_re = re.compile(define_format, re.I)
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
        all = [ l.strip().split('\t', 2) for l in open('factoids') ]
        facts = [ (how, fact) for key, how, fact in all
                  if key.lower() == what.lower() ]
        if not facts:
            reply = random.choice(huh).replace('%s', what)
            self.bot.core.reply(sender, where, reply)

        else:
            how, text = random.choice(facts)
            if text.startswith('<reply> '):
                self.bot.send('PRIVMSG %s :%s' % (where, text[8:]))
            elif text.startswith('<action> '):
                self.bot.core.action(where, text[9:])
            else:
                txt = 'Jeg mener helt bestemt at %s %s %s' % (what, how, text)
                self.bot.core.reply(sender, where, txt)
        
    def on_define(self, sender, where, what):
        m = define_re.match(what)
        if not m:
            txt = '%r <- FAT DET!' % define_format
            self.bot.core.reply(sender, where, txt)
            return True

        thing, how, text = m.groups()
        thing = thing.replace('\t', ' ')
        open('factoids', 'a').write('%s\t%s\t%s\n' % (thing, how, text))

        self.bot.core.got_it(sender, where)

    def on_list(self, sender, where, prefix):
        all = [ l.strip().split('\t', 1) for l in open('factoids') ]
        facts = {}
        for key, fact in all:
            if key.lower() in facts:
                continue
            if key.lower().startswith(prefix):
                facts[key.lower()] = key

        if facts:
            reply = 'Jeg ved ting om ' + ', '.join(facts.values())
        else:
            reply = 'No clue'
        self.bot.core.reply(sender, where, reply)

plugin = Factoid
