def print_input_output(fn):
    import collections

    def wrapper(*args, **kw_args):
        print 'debug decorator on', fn.__name__, '. args:', args
        print 'debug decorator on', fn.__name__, '. kw_args:', kw_args
        r = fn(*args, **kw_args)
        if isinstance(r, collections.Iterable):
            print 'debug decorator on', fn.__name__, '. res :', map(str,r)
        else:
            print 'debug decorator on', fn.__name__, '. res :', r
        return r

    return wrapper