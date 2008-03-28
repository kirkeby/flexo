# -*- encoding: utf-8 -*-

from __future__ import absolute_import

from time import localtime

import random

got_its = ['Yeeees, yes', 'Har det!', 'Oki', 'You speak wisely, sir']

def is_it_friday():
    return localtime().tm_wday == 4

def is_bot(nick):
    return nick == 'Bender'

def random_line(file):
    '''Retrieve a random line from a file, decoded as UTF-8 and stripped.'''
    return random_element(file).decode('utf-8').strip()
    
def random_element(iter):
    '''Retrieve a random item from an iterable object of unknown length,
    looping through it just once.'''

    it = None
    for i, e in enumerate(iter):
        if random.uniform(0, i + 1) < 1:
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
