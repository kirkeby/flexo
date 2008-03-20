# -*- encoding: utf-8 -*-
from __future__ import absolute_import

import re

def is_channel(name):
    return name and name[0] in '&#+!'

prefix = ':([^ ]+)'
command = '([a-zA-Z]+|[0-9]{3})'
middle = '((?: [^\0\r\n :][^\0\r\n ]*)*)'
trailing = '([^\0\r\n]+)'
message = '^(?:%s )?%s%s(?: :%s)?$' \
          % (prefix, command, middle, trailing)
message_re = re.compile(message)

def parse_message(message):
    m = message_re.match(message)
    if not m:
        raise ValueError('%r is not a valid IRC message')

    prefix, command, middle, trailing = m.groups()
    pieces = [ prefix, command, [] ]
    if middle:
        pieces[-1].extend(middle.strip().split())
    if trailing:
        pieces[-1].append(trailing)

    return pieces

def parse_prefix(prefix):
    if u'!' in prefix:
        return tuple(prefix.split('!', 1))
    else:
        return prefix, None

numerical_names = {
    u'001': u'WELCOME',
    u'004': u'MYINFO',
    u'353': u'NAMREPLY',
}

message_parameters = {
    u'PRIVMSG': ('channel', 'says',),
    u'QUIT': ('channel', 'reason',),
    u'JOIN': ('channel',),
    u'PART': ('channel', 'reason',),
    u'MODE': ('channel', 'mode', 'what'),
    u'TOPIC': ('channel', 'topic',),
    u'KICK': ('channel', 'target', 'reason'),
    u'NAMREPLY': ('nick', 'chantype', 'channel', 'names'),
    u'MYINFO': ('nick', 'servername',),
    u'PING': ('source',),
}
def parse_parameters(command, parameters):
    command = numerical_names.get(command, command)
    result = dict(zip(message_parameters.get(command, ()), parameters))
    return result
