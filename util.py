import re

y = 46


def parse_int(sin):
    m = re.search(r'^(\d+)[.,]?\d*?', str(sin))
    return int(m.groups()[-1]) if m and not callable(sin) else None


def nn(n):
    if n < 10:
        return '00' + str(n)
    else:
        if n < 100:
            return '0' + str(n)
        else:
            return str(n)


def mm(p):
    return (parse_int((p - 1) / 10) % 10) + (((p - 1) % 10) * 3)


def su(a, b, c):
    return str(a[b:b+c])


def lc(l):
    if len(l) != 2:
        return l

    az = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

    a = l[0:1]
    b = l[1:2]

    if a == 'Z':
        return str(8000 + az.index(b))
    else:
        return str(az.index(a) * 52 + az.index(b))


def initpage(cs):
    cs_len = len(cs)
    for i in range(int(cs_len/50)):
        if su(cs, i*50, 4):