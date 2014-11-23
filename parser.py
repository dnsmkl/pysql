import mkw


print map(str,mkw.mkw_retokenize_from_str('sel 1 , ( bla , dfd)'))




# TODO: IMPLEMENT!
def form_bracket_chunks(mkw_tokens):
    pass


def test_form_bracket_chunks():
    txt = 'sel 1 , ( bla , dfd)'
    mkws = mkw.mkw_retokenize_from_str(txt)
    chunks = form_bracket_chunks(mkws)

    assert(len(chunks) == 4)
    assert(isinstance(chunks[0],mkw.Mkw_Token) and chunks[0] == 'sel')
    assert(isinstance(chunks[1],mkw.Mkw_Token) and chunks[0] == '1')
    assert(isinstance(chunks[2],mkw.Mkw_Token) and chunks[0] == ',')
    assert(not isinstance(chunks[3],mkw.Mkw_Token))

if __name__ == '__main__':
    test_form_bracket_chunks()
