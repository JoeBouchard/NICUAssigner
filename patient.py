class Patient:
    def __init__(self, name='bar', attrs=[]):
        """name is a string of the Patient's name
        attrs is a list of the Patient's Attributes"""
        
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
