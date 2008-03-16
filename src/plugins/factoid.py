# -*- encoding: utf-8 -*-
import re
import random

from flexo.plugin import Plugin
from flexo.prelude import got_its

define_format = r'^!!\s*(.*?)\s+(er|har)\s+(.*)$'
define_re = re.compile(define_format, re.I)
huh = ['Huh?!', 'I know not this "%s" you speak of',
       'Aner det ikke', 'Kein ahnung',
       '<action> aner ikke hvad "%s" er']

class Factoid(Plugin):
    def on_public_msg(self, message):
        what = message.tail
        if what.startswith('!?'):
            what = what[2:].strip()
            self.on_lookup(message, what)
            return True

        elif what.startswith('!!'):
            self.on_define(message, what)
            return True

        elif what.startswith('!listfacts '):
            prefix = what.split(' ', 1)[1].strip()
            self.on_list(message, prefix.lower())
            return True

    def on_lookup(self, message, what):
        all = [ l.strip().decode('utf-8').split('\t', 2)
                for l in self.bot.open_state('factoids') ]
        facts = [ (how, fact) for key, how, fact in all
                  if key.lower() == what.lower() ]

        if not facts:
            reply = random.choice(huh).replace('%s', what)
        else:
            how, reply = random.choice(facts)
            if not reply.startswith(u'<'):
                reply = u'Jeg mener helt bestemt at %s %s %s' \
                        % (what, how, reply)
            reply = reply.replace('%s', message.nick)
        message.reply(reply)
        
    def on_define(self, message, what):
        m = define_re.match(what)
        if not m:
            txt = '%r <- FAT DET!' % define_format
            message.reply(txt)
            return True

        thing, how, text = m.groups()
        thing = thing.replace('\t', ' ')
        
        line = u'%s\t%s\t%s\n' % (thing, how, text)
        self.bot.open_state('factoids', 'a').write(line.encode('utf-8'))

        message.reply(random.choice(got_its))

    def on_list(self, message, prefix):
        all = [ l.strip().decode('utf-8').split('\t', 1)
                for l in self.bot.open_state('factoids') ]
        facts = {}
        for key, fact in all:
            if key.lower() in facts:
                continue
            if key.lower().startswith(prefix):
                facts[key.lower()] = key

        if facts:
            reply = u'Jeg ved ting om ' + ', '.join(facts.values())
        else:
            reply = u'Jeg kender ikke nogen ting som starter med "%s"' % prefix
        message.reply(reply)

plugin = Factoid
