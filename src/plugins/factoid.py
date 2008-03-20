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
    def on_privmsg(self, message):
        what = message.says

        if what.startswith('!?'):
            what = what[2:].strip()
            self.on_lookup(message, what)
            return True

        elif what.startswith('!!'):
            self.on_define(message, what)
            return True

        return Plugin.on_privmsg(self, message)

    def on_bang_listfacts(self, message, prefix):
        self.on_list(message, prefix.lower())
        return True

    def on_lookup(self, message, what):
        facts = [ (how, fact)
                  for key, how, fact in self.bot.read_state('factoids')
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
        self.bot.append_state('factoids', (thing, how, text))

        message.reply(random.choice(got_its))

    def on_list(self, message, prefix):
        all = [ key for key, how, fact in self.bot.read_state('factoids') ]

        facts = {}
        for key in all:
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
