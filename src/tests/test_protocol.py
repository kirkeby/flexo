from flexo.protocol import is_channel
from flexo.protocol import parse_message
from flexo.protocol import parse_prefix

def test_is_channel():
    assert is_channel('#cafeen')
    assert is_channel('&bitlbee')
    assert not is_channel('kirkeby')

def test_parse_prefixless():
    assert parse_message('PING 42') \
           == [None, 'PING', ['42']]
    assert parse_message('ERROR :Closing connection') \
           == [None, 'ERROR', ['Closing connection']]

def test_parse_without_trailing():
    assert parse_message(':localhost 001 Welcome.') \
           == ['localhost', '001', ['Welcome.']]
    assert parse_message(':localhost FURRFU abc:def') \
           == ['localhost', 'FURRFU', ['abc:def']]

def test_parse_with_trailing():
    assert parse_message(':localhost PRIVMSG #cafeen :!lart Bender') \
           == ['localhost', 'PRIVMSG', ['#cafeen', '!lart Bender']]
    assert parse_message(':localhost KICK #cafeen kirkeby : Uuuuuud!') \
           == ['localhost', 'KICK', ['#cafeen', 'kirkeby', ' Uuuuuud!']]

def test_parse_prefix():
    assert parse_prefix('localhost.localdomain') == ('localhost.localdomain', None)
    assert parse_prefix('kirkeby!~kirkeby') == ('kirkeby', '~kirkeby')
    assert parse_prefix('x!y@z') == ('x', 'y@z')
