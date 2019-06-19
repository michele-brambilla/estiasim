from __future__ import absolute_import

import functools

from pcaspysim.devices import log

string_types = str


def run_async(func):
    from threading import Thread
    from functools import wraps

    @wraps(func)
    def async_func(*args, **kwargs):
        handle = Thread(target=func, args=args, kwargs=kwargs)
        handle.start()
        return handle

    return async_func


class check_limits(object):
    def __init__(self, lower=False, upper=False, silent=False):
        self._lower = lower
        self._upper = upper
        self._silent = silent

    def __call__(self, f):
        @functools.wraps(f)
        def limit_checked(obj, new_value):
            lower = getattr(obj, self._lower) if isinstance(self._lower, str) \
                else self._lower
            upper = getattr(obj, self._upper) if isinstance(self._upper, str) \
                else self._upper
            if (lower is None or lower <= new_value) and (upper is None or
                                                          new_value <= upper):
                return f(obj, new_value)

            if not self._silent:
                log.error(
                    '{} is outside limits ({}, {})'.format(new_value, lower,
                                                           upper))

        return limit_checked


class Dummy(object):
    value = 0
    _low_limit = 0
    _high_limit = 1

    @property
    def low_limit(self):
        return self._low_limit

    @low_limit.setter
    def low_limit(self, value):
        self._low_limit = value

    @property
    def high_limit(self):
        return self._high_limit

    @high_limit.setter
    def high_limit(self, value):
        self._high_limit = value

    @check_limits('low_limit', 'high_limit')
    def move(self, target):
        self.value = target


if __name__ == '__main__':
    x = Dummy()

    print('before')
    x.move(10)
    x.move(-5)

    x.high_limit = 20
    x.low_limit = -10

    print('after')
    x.move(10)
    x.move(-5)
