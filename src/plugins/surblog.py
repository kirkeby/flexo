# vim:encoding=utf-8:

from flexo.plugin import Plugin

import os
from random import choice
from xml.sax.saxutils import escape

slug_words = [ w.strip() for w in open('state/surblog/slug-words') ]
def new_post_path():
    while True:
        slug = '-'.join(choice(slug_words) for i in range(3))
        path = os.path.join('state/surblog', slug) + '.txt'
        if not os.path.exists(path):
            break
    return path

class Surblog(Plugin):
    def on_topic(self, message):
        channel = message.channel.name
        reason = message.topic

        if not channel == u'#cafeen':
            return
        if not reason.startswith(u'Kvan er sur '):
            return

        line = escape(message.topic) + u'\n'
        path = new_post_path()
        open(path, 'w').write(line.encode('utf-8'))

plugin = Surblog
