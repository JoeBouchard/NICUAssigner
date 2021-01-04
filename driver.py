from tkinter import *
from nurse import *
from attributes import *
from patient import *

testing = True

class MainScreen:
    
    def __init__(self, name):
        self.tk = Tk(screenName=name, baseName=name)
        self.nurses = []
        self.attrs = []
        self.patients = []
        self.nurseFrame = Frame(self.tk)
        self.nurseDisplay = Listbox(self.nurseFrame)

        self.patientFrame = Frame(self.tk)
        self.patientDisplay = Listbox(self.patientFrame)
        self.pack()

    def addNurse(self, name, attrs):
        nurse = Nurse(name, attrs)
        self.nurses.append(nurse)

    def updateNurses(self):
        for nNum in range(0, len(self.nurses)):
            self.nurseDisplay.insert(nNum, self.nurses[nNum].getName())

    def pack(self):
        self.nurseLabel = Label(self.nurseFrame, text="Nurses:")
        self.nurseLabel.pack(side='top')
        self.nurseDisplay.pack(side='bottom')
        self.nurseFrame.pack(side='left')

        self.patientLabel = Label(self.patientFrame, text="Patients:")
        self.patientLabel.pack(side='top')
        self.patientDisplay.pack(side='bottom')
        self.patientFrame.pack(side='right')
    
        
m=MainScreen("Hello")

if testing:
    m.addNurse("Frida", ['a', 'b', 'c'])
    m.updateNurses()

