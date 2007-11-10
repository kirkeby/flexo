from time import localtime
from random import uniform

def is_it_friday():
    return localtime().tm_wday == 4

def random_element(iter):
    '''Retrieve a random item from an iterable object of unknown length,
    looping through it just once.'''

    it = None
    for i, e in enumerate(iter):
        if uniform(0, i) < 1:
            it = e

    return it

def get_nick_channel(context):
    if isinstance(context, tuple):
        return get_nick(context[0]), context[1]
    else:
        return get_nick(context), None
def get_nick(context):
    if isinstance(context, tuple):
        context = context[0]
    return context.split('!', 1)[0][1:]
