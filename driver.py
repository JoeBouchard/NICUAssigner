from tkinter import *
from nurse import *
from attributes import *

testing = True

class MainScreen:
    
    def __init__(self, name):
        self.tk = Tk(screenName=name, baseName=name)
        self.nurses = []
        self.attrs = []
        self.patients = []
        self.nurseDisplay = Listbox(self.tk)
        self.pack()

    def addNurse(self, name, attrs):
        nurse = Nurse(name, attrs)
        self.nurses.append(nurse)

    def updateNurses(self):
        for nNum in range(0, len(self.nurses)):
            self.nurseDisplay.insert(nNum, self.nurses[nNum].getName())


    def pack(self):
        self.nurseDisplay.pack()
    
        
m=MainScreen("Hello")

if testing:
    m.addNurse("Frida", ['a', 'b', 'c'])
    m.updateNurses()

