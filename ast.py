



class Node(object):
    children = None
    # def __init__(self)
    #     self.children = None


    def __str__(self):
        """Subclasses have to implement name attribute"""
        return self.name


class Statement(Node):
    name = "Statement"

class ClauseSelect(Node):
    name = "Select"

class ClauseFrom(Node):
    name = "From"

class ClauseWhere(Node):
    name = "Where"





print y
