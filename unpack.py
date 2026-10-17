#
# unpacking lists, sets et dicts
#
# $ python unpack.py
# [1, 2, 3, 4, 5]
# {1, 2, 3, 4}
# {'a': 3, 'b': 2}
#

def list_unpack():
    lists = [[1, 2], [3, 4], [5]]
    l = [*L for L in lists]
    print(l)
    # [1, 2, 3, 4, 5]
    # équivalent à [x for L in lists for x in L]

def set_unpack():
    sets = [{1, 2}, {2, 3}, {3, 4}]
    s = {*s for s in sets}
    print(s)
    # {1, 2, 3, 4}
    # équivalent à {x for s in sets for x in s}

def dict_unpack():
    dicts = [{'a': 1}, {'b': 2}, {'a': 3}]
    d = {**d for d in dicts}
    print(d)
    # {'a': 3, 'b': 2}
    # équivalent à {k: v for d in dicts for k,v in d.items()}

def unpack():
    list_unpack()
    set_unpack()
    dict_unpack()

if __name__=='__main__':
    unpack()