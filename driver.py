from tkinter import *
from nurse import *
from attributes import *
from patient import *

testing = True

class MainScreen:
    
    def __init__(self, name):
        self.tk = Tk(screenName=name, baseName=name)
        
        self.nurses = []
        self.patients = []
        
        self.nurseAttrs = []
        self.patientAttrs = []
        self.attrRelations = {}
        
        self.nurseFrame = Frame(self.tk)
        self.nurseDisplay = Listbox(self.nurseFrame)
        self.nurseAttrsDisplay = []
        self.nurseCheckVars = []
        self.nurseAttrsFrame = Frame(self.nurseFrame)

        self.patientFrame = Frame(self.tk)
        self.patientDisplay = Listbox(self.patientFrame)
        self.patientAttrsDisplay = []
        self.patientCheckVars = []
        self.patientAttrsFrame = Frame(self.patientFrame)
        
        self.pack()

    def getNurse(self, name):
        for n in self.nurses:
            if n.getName() == name:
                return n

    def addNurse(self, name, attrs):
        nurse = Nurse(name, attrs)
        self.nurses.append(nurse)
        for a in attrs:
            if a not in self.nurseAttrs:
                self.nurseAttrs.append(a)

        self.updateNurses()

    def updateNurses(self):
        self.nurseDisplay.delete(0, END)
        for nNum in range(0, len(self.nurses)):
            self.nurseDisplay.insert(nNum, self.nurses[nNum].getName())

        for a in self.nurseAttrs:
            found = False
            for b in self.nurseAttrsDisplay:
                if b.cget('text') == a:
                    found = True
                    break
            if not found:
                v=IntVar() 
                c=Checkbutton(self.nurseAttrsFrame, text=a, variable=v)
                self.nurseCheckVars.append(v)
                c.pack(side='top')
                self.nurseAttrsDisplay.append(c)
                print(a)

    def nurseSelect(self, event):
        w = self.nurseDisplay
        print(w, 'n')
        index = w.curselection()
        for i in index:
            name = w.get(i)
            nurse = self.getNurse(name)
            for b in self.nurseAttrsDisplay:
                b.deselect()
            for b in self.patientAttrsDisplay:
                b.deselect()
            for a in nurse.getAttrs():
                for b in self.nurseAttrsDisplay:
                    if b.cget('text') == a:
                        b.select()

    def getPatient(self, name):
        for n in self.patients:
            if n.getName() == name:
                return n
            
    def addPatient(self, name, attrs):
        patient = Patient(name, attrs)
        self.patients.append(patient)
        for a in attrs:
            if a not in self.patientAttrs:
                self.patientAttrs.append(a)
                
        self.updatePatients()

    def updatePatients(self):
        self.patientDisplay.delete(0, END)
        
        for pNum in range(0, len(self.patients)):
            self.patientDisplay.insert(pNum, self.patients[pNum].getName())

        for a in self.patientAttrs:
            found = False
            for b in self.patientAttrsDisplay:
                if b.cget('text') == a:
                    found = True
                    break
            if not found:
                v = IntVar()
                c=Checkbutton(self.patientAttrsFrame, text=a, variable=v)
                self.patientCheckVars.append(v)
                c.pack(side='top')
                self.patientAttrsDisplay.append(c)
                print(a)

    def patientSelect(self, event):
        w = self.patientDisplay
        print(w, 'p')
        index = w.curselection()
        for i in index:
            name = w.get(i)
            patient = self.getPatient(name)
            for b in self.nurseAttrsDisplay:
                b.deselect()
            for b in self.patientAttrsDisplay:
                b.deselect()
            for a in patient.getAttrs():
                for b in self.patientAttrsDisplay:
                    if b.cget('text') == a:
                        b.select()
                        print(a)

    def pack(self):
        self.nurseLabel = Label(self.nurseFrame, text="Nurses:")
        self.nurseLabel.pack(side='top')
        self.nurseDisplay.pack(side='left')
        self.nurseAttrsFrame.pack(side='right')
        self.nurseFrame.pack(side='left')
        self.nurseDisplay.bind('<<ListboxSelect>>', self.nurseSelect)

        self.patientLabel = Label(self.patientFrame, text="Patients:")
        self.patientLabel.pack(side='top')
        self.patientDisplay.pack(side='right')
        self.patientAttrsFrame.pack(side='left')
        self.patientFrame.pack(side='right')
        self.patientDisplay.bind('<<ListboxSelect>>', self.patientSelect)
    
        
m=MainScreen("Hello")

if testing:
    m.addNurse("Frida", ['a', 'b', 'c'])
    m.addNurse("Franz", ['a', 'c'])
    m.addNurse("Fred", ['b', 'c'])
    
    m.addPatient("Claude", ['d', 'e', 'f'])

