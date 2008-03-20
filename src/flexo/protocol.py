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
