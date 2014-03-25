"""
Fantail
"""
# -*- coding: utf-8 -*-

from __future__ import print_function


class Fanstack(object):

    def __init__(self, stack=None):

        if stack is None:
            self.stack = []
        else:
            self.stack = stack

    def __getitem__(self, key):
        for s in self.stack:
            if key in s:
                return s[key]
        raise KeyError(key)

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
