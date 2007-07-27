import time
import random

def is_it_friday():
    return time.localtime().tm_wday == 4

def random_element(iter):
    '''Retrieve a random item from an iterable object of unknown length,
    looping through it just once.'''

    it = None
    for i, e in enumerate(iter):
        if random.uniform(0, i) < 1:
            it = e

    return it
