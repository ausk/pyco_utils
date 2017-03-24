import os
import sys
import string
import random


def pardir(path, depth=1):
    path = os.path.abspath(path)
    for i in range(depth):
        path = os.path.dirname(path)
    return path


def source_root(path):
    sys.path.insert(0, path)


def short_uuid(length):
    charset = string.ascii_letters + string.digits
    return ''.join([random.choice(charset) for i in range(length)])


def str2list(text, line_sep='\n', strip_chars=None, filter_func=None):
    paras = [x.strip(strip_chars) for x in text.split(line_sep)]
    data = list(filter(filter_func, paras))
    return data


def list2dict(lines, sep=':', strip_chars=None):
    result = {}
    for i, line in enumerate(lines):
        paras = line.split(sep)
        k = paras[0].strip(strip_chars)
        v = ':'.join(paras[1:]).strip(strip_chars)
        result[k] = v
    return result


def str2dict(text, line_sep='\n', dict_sep=':'):
    ls = str2list(text, line_sep)
    ds = list2dict(ls, dict_sep)
    return ds


def fetch_dict(form, keys, default=None):
    ds = {}
    for k in keys:
        v = form.get(k, default)
        ds[k] = v
    return ds


# eg : mysql.proxy rows

def sort_rows(rows, key):
    # python2 cmp
    # func = lambda a, b: cmp(a.get(key), b.get(key))
    # ds = sort(rows, cmp=func)
    # python3, cmp is deprecated
    func = lambda x: x.get(key)
    ds = sorted(rows, key=func)
    return ds


def include(form, query):
    for k, v in query.items():
        dv = form.get(k)
        if dv != v:
            return False
    return True


def filter_rows(rows, query):
    from functools import partial
    func = partial(include, query=query)
    ds = list(filter(func, rows))
    return ds