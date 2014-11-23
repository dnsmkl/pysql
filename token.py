class Token(object):
    def __init__(self, text, token_type, cnt_consumed=None):
        self.cnt_consumed = cnt_consumed if cnt_consumed else len(text)
        self.text = text
        self.type = token_type

    def __repr__(self):
        # return 't("{}", {})'.format(self.text, self.is_keyword)
        return str((str(self.text), self.type, self.cnt_consumed))

    def __str__(self):
        # return 't("{}", {})'.format(self.text, self.is_keyword)
        return str(self.text)

    def __eq__(self, other):
        return str(self) == str(other)

    def __len__(self):
        return len(self.text)