# coding: utf-8

import time
from pprint import pformat
import threading
from functools import (
    wraps,
    reduce,
)

from werkzeug.exceptions import (
    TooManyRequests,
    GatewayTimeout,
    RequestTimeout,
)


# 注意 wraps 是必须的。

def ajax_func(func, daemon=True):
    @wraps(func)
    def wrapper(*args, **kwargs):
        th = threading.Thread(target=func, args=args, kwargs=kwargs)
        th.daemon = daemon
        th.start()

    return wrapper


def singleton(cls):
    '''
    # 使用这个装饰器的类，不能作为父类被继承
    @singleton
    class Settings(object):
        pass
    '''
    instance = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instance:
            instance[cls] = cls(*args, **kwargs)
        return instance[cls]

    return get_instance


def log_time(func):
    '''
    @log_time
    def func():
        pass
    '''
    t1 = time.time()

    @wraps(func)
    def wrapper(*args, **kwargs):
        m = func(*args, **kwargs)
        t2 = time.time()
        tm = t2 - t1
        msg = '{}, {}ms \n<{}>\n'.format(func.__name__, tm, pformat(m))
        print(msg)
        return m

    return wrapper


def retry(func, count=3):
    '''
    @retry
    def func():
        pass
    '''
    from .colog import format_func

    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(count - 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                m = format_func(func.__name__, *args, **kwargs)
                print('[retry Error]\t{}\n\{}'.format(e, m))
        return func(*args, **kwargs)

    return wrapper


def retry_api(count=3, delay=30, exceptions=None):
    '''
    @retry_api()
    def fac(n):
        m = reduce(lambda x, y: x * y, range(1, n + 1))
        return m
    '''
    if exceptions is None:
        exceptions = (
            RequestTimeout,
            GatewayTimeout,
            TooManyRequests,
        )

    def deco(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(count - 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return deco


def _retry_api(func, count=3, delay=30, exceptions=None):
    '''
    @_retry_api
    def fac(n):
        m = reduce(lambda x, y: x * y, range(1, n + 1))
        return m

    '''
    if exceptions is None:
        exceptions = (
            RequestTimeout,
            GatewayTimeout,
            TooManyRequests,
        )

    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(count - 1):
            try:
                return func(*args, **kwargs)
            except exceptions as e:
                time.sleep(delay)

        return func(*args, **kwargs)

    return wrapper
