# vim:encoding=utf-8:

import re
from threading import Thread
from urllib import urlopen
from urllib import quote

from flexo.plugin import Plugin

import logging
log = logging.getLogger('flexo.plugins.ro')

# FIXME - tråde henover en graceful restart er nok ikke verdens bedste plan.
def _fetch(url, callback):
    try:
        file = urlopen(url)
        content = file.read()
        file.close()
        
        callback(content)

    except:
        log.exception('URL fetcher')
        callback(None)

def fetch(url, callback):
    log.debug('Fetching %s' % url)
    t = Thread(target=_fetch, name='URL fetcher', args=(url, callback))
    t.start()

ro_url = 'http://retskrivningsordbogen.dk/ro/dataservlet?p1=%s&p2=false&p3=0&p4=10'
ro_outer_rex = re.compile(r'<p>(.*)</p>')
ro_tag_rex = re.compile(r'<[^>]+>')
ro_max_artikler = 3
class Staveplade(Plugin):
    def on_bang_ro(self, message, ord):
        def reply(result):
            if result is None:
                message.reply(u'Det fejlede :(')

            else:
                soup = ro_outer_rex.search(result).group(0)
                artikler = [ ro_tag_rex.sub('', a)
                             for a in soup.split('</p><p>') ]
                
                text = '; '.join(artikler[ : ro_max_artikler])
                if len(artikler) > ro_max_artikler:
                    text = text + '; [..]'
                
                message.reply(text.decode('latin-1'))

        url = ro_url % quote(ord.encode('utf-8'))
        fetch(url, reply)

plugin = Staveplade
