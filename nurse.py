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
        self.attrs.append(attr)

    def removeAttr(self, attr):
        self.attrs.remove(attr)

    def __lt__(self, other):
        return self.getName() < other.getName()

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.getName() == other.getName()
        return self.getName() == other
