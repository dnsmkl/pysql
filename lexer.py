from debug import print_input_output

from token import Token



keyword_list = ['from','join','inner','right','cross','left','outer','full','as']


# @print_input_output
def tokenize(text):
    i = 0
    puntuation_start = map(lambda x: x[0], punctuation)
    while i < len(text):

        if text[i] in spacing: r = Token(eat_spacing(text[i:]), 'space or comment')
        elif text[i:i+2] == '--': r = Token(eat_comment_oneline(text[i:]), 'space or comment')
        elif text[i:i+2] == '/*': r = Token(eat_comment_multiline(text[i:]), 'space or comment')
        elif text[i] in puntuation_start: r = Token(eat_punctuation(text[i:]), 'punctuation')
        elif text[i] in "'": r = Token(eat_string(text[i:]), 'string')
        elif text[i] in '"': r = Token(eat_string_doubleq(text[i:]), 'string_doubleq')
        else: r = Token(eat_words(text[i:]), "id")

        if r.text.lower() in keyword_list: r.type = "keyword"

        i += len(r)
        yield r


@print_input_output
def ltokenize(text):
    return list(tokenize(text))


def eat_comment_oneline(text): return _eat_start_end(text, '--', '\n', False)


def test_eat_comment_oneline():
    eat = eat_comment_oneline

    assert eat('--') == '--'
    assert eat('--\ntext after comment') == '--\n'
    assert eat('--comment text\ntext after comment') == '--comment text\n'
    assert eat('--comment text\n--next comment\ntext after comment') == '--comment text\n'



def eat_comment_multiline(text): return _eat_start_end(text, '/*', '*/', False)


def test_eat_comment_multiline():
    eat = eat_comment_multiline

    assert eat('/*') == '/*'
    assert eat('/*\ntext after comment start') == '/*\ntext after comment start'
    assert eat('/*comment text*/\ntext after comment') == '/*comment text*/'
    assert eat('/*comment text\n*//*next comment*/\ntext after comment') == '/*comment text\n*/'


punctuation = ['==','<=','>=','<>','!=','||','=','<','>','(',')','/','*','-','+',',',';','?']
def eat_punctuation(text):
    for i in xrange(len(text)):
        if i < len(text) and text[i:i+2] in punctuation: return text[0:i+2]
        if text[i] in punctuation: return text[i]
    else:
        assert 0 # This should never be reached


def test_eat_punctuation():
    eat = eat_punctuation
    assert eat('==') == '=='
    assert eat('= =') == '='
    assert eat('>=') == '>='
    assert eat('=>') == '='


def eat_string(text): return _eat_start_end(text, "'", "'", True)


def test_eat_string():
    eat = eat_string

    assert eat("''") == "''"
    assert eat("'") == "'"
    assert eat("'bnbn") == "'bnbn"
    assert eat("'bnbn''dfdf") == "'bnbn''dfdf"
    assert eat("'bnbn''dfdf'") == "'bnbn''dfdf'"
    assert eat("'bnbn''dfdf'353535") == "'bnbn''dfdf'"
    assert eat("'bnbn' 'dfdf'353535") == "'bnbn'"



def eat_string_doubleq(text): return _eat_start_end(text, '"', '"', True)


def test_eat_string_doubleq():
    eat = eat_string_doubleq

    assert eat('""') == '""', eat('""')
    assert eat('"') == '"'
    assert eat('"bnbn') == '"bnbn'
    assert eat('"bnbn""dfdf') == '"bnbn""dfdf'
    assert eat('"bnbn""dfdf"') == '"bnbn""dfdf"'
    assert eat('"bnbn""dfdf"353535') == '"bnbn""dfdf"'
    assert eat('"bnbn" "dfdf"353535') == '"bnbn"'


spacing = ' \n\t'

def eat_words(text):
    nonwordchars = []
    nonwordchars.extend(spacing)
    nonwordchars.extend(map(lambda x: x[0], punctuation))

    assert text[0] not in nonwordchars
    for i, c in enumerate(text):
        if c in nonwordchars: return text[0:i]
    else:
        return text


def test_eat_words():
    eat = eat_words
    assert eat('a') == 'a'
    assert eat('a a') == 'a'
    assert eat('a123b.1234, a') == 'a123b.1234'


def eat_spacing(text): return _eat_valid(text, spacing, "")


def test_eat_spacing():
    eat = eat_spacing
    assert eat(' ') == ' '
    assert eat(' a') == ' '
    assert eat('\na') == '\n'
    assert eat('\n a') == '\n '
    assert eat(' \n a') == ' \n '
    assert eat(' \na a') == ' \n'



def _eat_start_end(text, start, end, join_adjacent):
    # delimiter lengths
    lstart = len(start)
    lend = len(end)

    assert text[0:len(start)] == start

    i = lstart
    while i < len(text):
        if i >= lstart and text[i-lend+1:i+1] == end:
            # check for the next `start`
            if join_adjacent:
                if len(text) > i + lstart and text[i+1:i+1+lstart] == start:
                    i += lstart + 1
                    continue
            return text[0:i+1]
        i += 1
    else:
        return text



def _eat_valid(text, valid, not_valid):
    assert text[0] in valid
    for i, c in enumerate(text):
        if c not in valid: return text[0:i]
    else:
        return text



    for i in xrange(len(text)):
        if i < len(text) and text[i:i+2] in punctuation: return text[0:i+2]
        if text[i] in punctuation: return text[i]
    else:
        assert 0 # This should never be reached



def main():
    # for t in tokenize("FROM table1 as alias1 JOIN table2 alias2 LEFT JOIN (sel 1)"):
    #     print t
    test_eat_comment_oneline()
    test_eat_comment_multiline()
    test_eat_punctuation()
    test_eat_string()
    test_eat_string_doubleq()
    test_eat_words()
    test_eat_spacing()
    print("Lexer - All tests passed.")

    input_text = "select a1 as --\n ,b /*cmt*/ from ((x)"
    r = ltokenize(input_text)
    assert(''.join(map(str,r)) == input_text)

if __name__ == '__main__':
    main()
