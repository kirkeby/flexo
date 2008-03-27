# vim:encoding=utf-8:

import re
from threading import Thread
from urllib import urlopen

from flexo.plugin import Plugin

# FIXME - tråde henover en graceful restart er nok ikke verdens bedste plan.
def _fetch(url, callback):
    try:
        file = urlopen(url)
        content = file.read()
        file.close()
        
        callback(content)

    except:
        callback(None)
def fetch(url, callback):
    t = Thread(target=_fetch, name='URL fetcher', args=(url, callback))
    t.start()

ro_url = 'http://retskrivningsordbogen.dk/ro/dataservlet?p1=%s&p2=false&p3=0&p4=10'
ro_outer_rex = re.compile(r'<p>(.*)</p>')
ro_tag_rex = re.compile(r'<[^>]+>')
class Staveplade(Plugin):
    def on_bang_ro(self, message, ord):
        def reply(result):
            if result is None:
                message.reply(u'Det fejlede :(')

            else:
                soup = ro_outer_rex.search(result).group(0)
                artikler = soup.split('</p><p>')
                for artikel in artikler:
                    text = ro_tag_rex.sub('', artikel)
                    message.reply(text.decode('latin-1'))

        fetch(ro_url % ord.encode('latin-1'), reply)

plugin = Staveplade
