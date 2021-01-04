class Nurse:
    def __init__(self, name='foo', attrs=[]):
        """name is a string of the Nurse's name
        attrs is a list of the Nurse's Attributes"""
        
        self.name = name
        self.attrs = attrs

    def getName(self):
        return self.name

    def getAttrs(self):
        return self.attrs

    def addAttr(self, attr):
        self.attrs.append(attrs)

    def __lt__(self, other):
        return self.getName() < other.getName()
