"""
Fantail
"""
# -*- coding: utf-8 -*-

from __future__ import print_function
from copy import copy

def merger(a, b):

    if a is None:
        return copy(b)

    if b is None:
        return copy(a)

    # if not type(a) == type(b):
    #     print(a, b)
    #     print(type(a))
    #     print(type(b))

    if isinstance(a, dict) and isinstance(b, dict):
        a = copy(a)
        a.update(b)

    if isinstance(a, list) and isinstance(b, list):
        a = copy(a)
        for item in b:
            if not item in a:
                a.append(item)
        return a

    #not updateable - return the first version
    return a



class Fanstack(object):

    def __init__(self, stack=None, mode='merge'):

        #how to deal with mergeable objects.
        #mode = merge -> attempt to merge
        #       top -> return first object seen
        #

        self.mode = mode
        if stack is None:
            self.stack = []
        else:
            self.stack = stack


    def __getitem__(self, key):

        rv = None

        for s in self.stack:
            if key in s:
                if self.mode == 'top':
                    return s[key]
                elif self.mode == 'merge':
                    rv = merger(rv, s[key])

        if rv is None:
            raise KeyError(key)

        return rv

    def __setitem__(self, key, value):
        self.stack[0].__setitem__(key, value)

    def get(self, key, default=None):
        for s in self.stack:
            if key in s:
                return s[key]
        return default

    def has_key(self, key):
        for s in self.stack:
            if key in s:
                return True
        return False

    def keys(self):
        k = set()
        for s in self.stack:
            k.update(set(s.keys()))
        return iter(list(k))

    def __contains__(self, key):
        return self.has_key(key)

    def update(self, d=None, **kwargs):
        if d is None:
            pass
        elif isinstance(d, dict):
            self.stack[0].update(d)
        if len(kwargs):
            self.stack[0].update(kwargs)
