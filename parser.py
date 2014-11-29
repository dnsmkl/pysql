import mkw


class Chunk(object):
    cstart = '('
    cend = ')'

    def __init__(self, payload):
        self.payload = payload

    def __str__(self):
        return str(payload)

    def mapstr(self):
        return map(str, self.payload)


def count_until_cstart(mkw_tokens, i, cstart):
    while True:
        if i >= len(mkw_tokens):
            break
        if mkw_tokens[i] == cstart:
            break
        i += 1
    return i


def count_through_chunk(mkw_tokens, i, cstart, cend):
    sub = 0
    assert mkw_tokens[i] == cstart
    while True:
        if i >= len(mkw_tokens):
            break
        if mkw_tokens[i] == cstart:
            sub += 1
        if mkw_tokens[i] == cend:
            sub -= 1
            if sub == 0:
                break
        i += 1
    return i


def form_chunks(mkw_tokens, cstart='(', cend=')'):
    r = list()
    i = 0
    while i < len(mkw_tokens):
        c_start_i = count_until_cstart(mkw_tokens, i, cstart)
        r.extend(mkw_tokens[i:c_start_i])
        if c_start_i >= len(mkw_tokens):
            break
        c_end_i = count_through_chunk(mkw_tokens, c_start_i, cstart, cend)
        c = Chunk(mkw_tokens[c_start_i:c_end_i+1])
        r.append(c)
        i = c_end_i + 1
    return r


import unittest


class TestBracketChunks(unittest.TestCase):

    def test_nested_heterogenus(self):
        txt = 'sel case (22=22) end'
        mkws = mkw.mkw_retokenize_from_str(txt)
        # self.assertEqual(len(mkws), 8)
        chunks = form_chunks(mkws)

        # self.assertEqual(len(chunks), 2) # sel <case> # 2 items
        # self.assertEqual(str(chunks[0]), 'sel')
        # self.assertEqual(len(chunks[1]), 3) # case <brackets> end # total 3 items
        # self.assertEqual(len(chunks[1][2]), 5) # ( 22 = 22 ) # total 5 items

    def test_nested_repeated_homogenous(self):
        txt = 'sel 1, (()) , ( bla , dfd ,'
        mkws = mkw.mkw_retokenize_from_str(txt)
        self.assertEqual(len(mkws), 13)
        chunks = form_chunks(mkws)

        self.assertEqual(len(chunks), 6)
        self.assertEqual(str(chunks[0]), 'sel')
        self.assertEqual(str(chunks[1]), '1')
        self.assertEqual(str(chunks[2]), ',')
        self.assertEqual(chunks[3].mapstr(), ['(','(',')',')'])
        self.assertEqual(str(chunks[4]), ',')
        self.assertEqual(chunks[5].mapstr(), ['(','bla',',','dfd',','])

    def test_simple(self):
        txt = 'sel 1 , ( bla , dfd ,'
        mkws = mkw.mkw_retokenize_from_str(txt)
        self.assertEqual(len(mkws), 8)
        chunks = form_chunks(mkws)

        self.assertEqual(str(chunks[0]), 'sel')
        self.assertEqual(str(chunks[1]), '1')
        self.assertEqual(str(chunks[2]), ',')
        self.assertEqual(chunks[3].mapstr(), ['(','bla',',','dfd',','])
        self.assertEqual(len(chunks), 4)


if __name__ == '__main__':
    unittest.main()
