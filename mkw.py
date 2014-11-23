'''
Define function `mkw_retokenize`.
Input:
- `Token`s
Result:
- multiword keywords are joined into one `Token`
- spacing and comments are removed
(TODO: make spacing and comments hidden part of `Token`)
'''


import lexer
import token


Mkw_Token = token.Token


def mkw_retokenize(tokens):
    ts = list(tokens)
    i = 0
    r = list()
    while i < len(ts):
        mkw_token = _eat_mkw_try_all(ts[i:])
        r.append(mkw_token)
        i += r[-1].cnt_consumed
    return r


g_mkws = list()
g_mkws.append(['full','outer','join'])
g_mkws.append(['right','outer','join'])
g_mkws.append(['left','outer','join'])
g_mkws.append(['full','join'])
g_mkws.append(['right','join'])
g_mkws.append(['left','join'])
g_mkws.append(['cross','join'])
g_mkws.append(['inner','join'])


def _eat_mkw_try_all(tokens):
    ts = list(tokens)
    for mkw in g_mkws:
        r = __eat_mkw_try_specified(ts, mkw)
        if r: return r
    # `__eat_mkw_try_specified` didn't find anything - `cnt_consumed` must be set here.
    ts[0].cnt_consumed = 1
    return __eat_token_as_mkw(ts)


def _test_eat_mkw_try_all():
    assert(_eat_mkw_try_all(lexer.tokenize('LEFT JOIN')) == 'LEFT JOIN')


def __eat_mkw_try_specified(tokens, mkw):
    ts = list(tokens)

    cnt_consumed = 0
    i = 0
    r = list()
    for t in ts:
        cnt_consumed += 1
        if t.type == 'space or comment': continue

        # Check for match of individual words.
        if t.text.lower() == mkw[i].lower():
            i += 1
            r.append(t.text)
        else:
            return None

        # Check if full mkw was matched.
        if i == len(mkw):
            return Mkw_Token(
                text=' '.join(r)
                , token_type='keyword'
                , cnt_consumed=cnt_consumed
            )


def __test__eat_mkw_try_specified():
    assert(
        __eat_mkw_try_specified(lexer.tokenize('LEFT JOIN'), ['LEFT', 'JOIN'])
        == 'LEFT JOIN'
    )
    assert(
        __eat_mkw_try_specified(lexer.tokenize('LEFT JOIN'), ['NO', 'MATCH'])
        == None
    )


def __eat_token_as_mkw(tokens):
    '''Eat one token, which is neither spacing and nor comment'''
    ts = list(tokens)
    cnt_consumed = 0
    i = 0
    r = list()
    for t in ts:
        cnt_consumed += 1
        if t.type == 'space or comment':
            # Skip spacing and comments
            continue
        else:
            i += 1
            t.cnt_consumed = cnt_consumed
            return t
    return None # Mark end of token list.


def __test__eat_token_as_mkw():
    assert(__eat_token_as_mkw(lexer.tokenize('LEFT JOIN')) == 'LEFT')
    assert(__eat_token_as_mkw(lexer.tokenize(' ')) == None)



def mkw_retokenize_from_str(text):
    return mkw_retokenize(lexer.tokenize(text))


def demo():
    print("MKW - Demo.")
    x = 'FROM table1 as alias1 JOIN table2 alias2 LEFT JOIN table3 RIGHT OUTER JOIN  table4 CROSS JOIN (FROM table5 INNER JOIN table6)'
    # x = 'LEFT JOIN'
    print('\n'.join(map(repr,mkw_retokenize(lexer.tokenize(x)))))


if __name__ == '__main__':
    _test_eat_mkw_try_all()
    __test__eat_mkw_try_specified()
    __test__eat_token_as_mkw()
    print('MKW - All tests passed.')
    demo()

