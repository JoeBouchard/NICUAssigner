from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from nurse import *
from attributes import *
from patient import *

testing = True

class MainScreen:
    
    def __init__(self, name):
        ##Create a base window everything is built on
        self.tk = Tk(screenName=name, baseName=name)
        self.tk.title(name)

        ##Create variables to store lists of nurses and patients
        self.nurses = []
        self.patients = []

        ##Create variables to store possible attributes of nurses and patients
        self.nurseAttrs = []
        self.patientAttrs = []
        self.attrRelations = {}

        ##Create display for nurse names and attributes
        self.nurseFrame = Frame(self.tk)
        self.nurseDisplay = Listbox(self.nurseFrame)
        self.nurseAttrsDisplay = []
        self.nurseCheckVars = []
        self.nurseAttrsFrame = Frame(self.nurseFrame)
        ##Create buttons to modify nurses
        self.addNurseBtn = Button(self.nurseFrame, text="Add Nurse")
        self.editNurseBtn = Button(self.nurseFrame, text="Edit Nurse")
        self.removeNurseBtn = Button(self.nurseFrame, text="Remove Nurse")

        ##Create display for patient names and attributes
        self.patientFrame = Frame(self.tk)
        self.patientDisplay = Listbox(self.patientFrame)
        self.patientAttrsDisplay = []
        self.patientCheckVars = []
        self.patientAttrsFrame = Frame(self.patientFrame)
        ##Create buttons to modify patients
        self.addPatientBtn = Button(self.patientFrame, text="Add Patient")
        self.editPatientBtn = Button(self.patientFrame, text="Edit Patient")
        self.removePatientBtn = Button(self.patientFrame, text="Remove Patient")

        ##Pack all to make it visible
        self.pack()

    def getNurse(self, name):
        """Returns Nurse object with the given name"""
        for n in self.nurses:
            if n.getName() == name:
                return n

    def addNurse(self, name, attrs):
        """Adds Nurse with name and attributes and updates the nurse display"""
        nurse = Nurse(name, attrs)
        self.nurses.append(nurse)
        for a in attrs:
            if a not in self.nurseAttrs:
                self.nurseAttrs.append(a)

        self.updateNurses()

    def removeNurse(self, name):
        self.nurses.remove(self.getNurse(name))
        self.updateNurses()

    def __addNurseBtn(self):
        """Button event to add a nurse"""
        name= simpledialog.askstring("Nurse name", "What is the nurse's name?")
        if name:
            self.addNurse(name, [])
            self.nurseDisplay.focus()
            self.nurseDisplay.selection_clear(0, END)
            self.nurseDisplay.selection_set(self.nurses.index(self.getNurse(name)))
            self.nurseDisplay.activate(self.nurses.index(self.getNurse(name)))
            print(self.nurses.index(self.getNurse(name)))
            print(self.nurseDisplay.curselection())
            self.__nurseSelect(0)
            self.__editNurseBtn(fromAdd=True)

    def __editNurseBtn(self, fromAdd=False):

        
        toggle = self.editNurseBtn.cget('text')

        print(toggle)
        if toggle == 'Edit Nurse':
            self.editNurseBtn.config(text='Finished Editing')
            for b in self.nurseAttrsDisplay:
                b.config(state='active')

        elif not fromAdd:
            self.editNurseBtn.config(text='Edit Nurse')
            for b in self.nurseAttrsDisplay:
                b.config(state='disabled')

    def __removeNurseBtn(self):
        
        w = self.nurseDisplay
        index = w.curselection()

        name = w.get(index)
        self.removeNurse(name)

    def __nurseCheckBtn(self):
        
        ##Get selected nurse
        w = self.nurseDisplay
        index = w.curselection()

        name = w.get(index)
        nurse = self.getNurse(name)
        
        selAttr = []
        for b in self.nurseAttrsDisplay:
            bVar = b.cget('var')
            isSelected = self.tk.getint(self.tk.getvar(bVar))

            if isSelected != 0:
                if b.cget('text') not in nurse.getAttrs():
                    nurse.addAttr(b.cget('text'))

            if isSelected == 0:
                if b.cget('text') in nurse.getAttrs():
                    nurse.removeAttr(b.cget('text'))
        

    def updateNurses(self):
        """refreshes the nurse display"""
        ##Add new nurses to the display
        self.nurses.sort()
        for nNum in range(0, len(self.nurses)):
            if self.nurses[nNum].getName() not in self.nurseDisplay.get(0, END):
                self.nurseDisplay.insert(nNum, self.nurses[nNum].getName())

        for nNum in range(0, self.nurseDisplay.size()):
            if self.nurseDisplay.get(nNum) not in self.nurses:
                self.nurseDisplay.delete(nNum)

        ##Iterate through all possible nurse attributes 
        for nA in range(0, len(self.nurseAttrs)):
            a = self.nurseAttrs[nA]
            found = False
            ##Find if the attribute already has a button
            for b in self.nurseAttrsDisplay:
                if b.cget('text') == a:
                    found = True
                    break
            ##Create a button if there isn't one
            if not found:
                v=IntVar() 
                c=Checkbutton(self.nurseAttrsFrame, text=a, variable=v, state='disabled')
                
                c.config(command=self.__nurseCheckBtn)
                self.nurseCheckVars.append(v)
                
                c.pack(side='top')
                self.nurseAttrsDisplay.append(c)
                print(a, self.nurseAttrs[nA])

    def __nurseSelect(self, event):
        """Toggle correct attributes when a nurse is selected"""
        ##Get selected nurse
        w = self.nurseDisplay
        index = w.curselection()
        
        ##For every selected nurse
        for i in index:
            ##Get name and object
            name = w.get(i)
            nurse = self.getNurse(name)
            
            ##Deselect all attributes
            for b in self.nurseAttrsDisplay:
                b.deselect()
            for b in self.patientAttrsDisplay:
                b.deselect()
                
            ##Select the nurse's attributes
            for a in nurse.getAttrs():
                for b in self.nurseAttrsDisplay:
                    if b.cget('text') == a:
                        b.select()

    def getPatient(self, name):
        """Returns a patient object given a name"""
        for n in self.patients:
            if n.getName() == name:
                return n
            
    def addPatient(self, name, attrs):
        """Adds patient with given name and attributes and updates the patient display"""
        ##Create new Patient
        patient = Patient(name, attrs)
        self.patients.append(patient)
        ##Add new attributes to attribute list
        for a in attrs:
            if a not in self.patientAttrs:
                self.patientAttrs.append(a)

        ##Update the display
        self.updatePatients()

    def updatePatients(self):
        """Updates display of patients"""

        ##Clear patient display
        self.patients.sort()
        self.patientDisplay.delete(0, END)

        ##Add all patients back in
        for pNum in range(0, len(self.patients)):
            self.patientDisplay.insert(pNum, self.patients[pNum].getName())

        ##Iterate through all patient attributes
        for a in self.patientAttrs:
            found = False
            
            ##Find if the attribute already has a checkbutton
            for b in self.patientAttrsDisplay:
                if b.cget('text') == a:
                    found = True
                    break
                
            ##Create a checkbutton if one doesn't exist
            if not found:
                v = IntVar()
                c=Checkbutton(self.patientAttrsFrame, text=a, variable=v, state='disabled')
                self.patientCheckVars.append(v)
                c.pack(side='top')
                self.patientAttrsDisplay.append(c)
                print(a)

    def __patientSelect(self, event):
        """Define event when patient is selected"""
        ##Get selected patient
        w = self.patientDisplay
        index = w.curselection()

        ##Deselect all buttons
        for b in self.nurseAttrsDisplay:
                b.deselect()
        for b in self.patientAttrsDisplay:
                b.deselect()
                
        ##Iterate through all selected
        for i in index:
            ##Get patient name and object
            name = w.get(i)
            patient = self.getPatient(name)

            ##Select appropriate attributes
            for a in patient.getAttrs():
                for b in self.patientAttrsDisplay:
                    if b.cget('text') == a:
                        b.select()
                        print(a)

    def pack(self):
        """Puts all created objects on the main screen"""
        ##Create text saying "Nurses:" to label the nurses section of the widget
        self.nurseLabel = Label(self.nurseFrame, text="Nurses:")
        self.nurseLabel.pack(side='top')
        
        ##Add nurse buttons to bottom of the display in reverse order
        self.removeNurseBtn.pack(side='bottom', fill='x')
        self.editNurseBtn.pack(side='bottom', fill='x')
        self.addNurseBtn.pack(side='bottom', fill='x')
        self.addNurseBtn.config(command=self.__addNurseBtn)
        self.editNurseBtn.config(command=self.__editNurseBtn)
        self.removeNurseBtn.config(command=self.__removeNurseBtn)
        
        ##Add the nurse list to the display on the left
        self.nurseDisplay.pack(side='left')
        
        ##Add frame with checkbuttons on the right
        self.nurseAttrsFrame.pack(side='right')
        
        ##Add frame with all nurse data on the left of the main widget
        self.nurseFrame.pack(side='left')
        
        ##Bind the __nurseSelect function to trigger when a nurse is selected
        self.nurseDisplay.bind('<<ListboxSelect>>', self.__nurseSelect)


        ##Create text saying "Patients:" to label the patients section of the widget
        self.patientLabel = Label(self.patientFrame, text="Patients:")
        self.patientLabel.pack(side='top')
        
        ##Add patient buttons in reverse order
        self.removePatientBtn.pack(side='bottom', fill='x')
        self.editPatientBtn.pack(side='bottom', fill='x')
        self.addPatientBtn.pack(side='bottom', fill='x')
        
        ##Add the pateint list to the right of the frame
        self.patientDisplay.pack(side='right')
        
        ##Add the button frame to the left of the frame
        self.patientAttrsFrame.pack(side='left')

        ##Add the patient frame on the right of the main screen
        self.patientFrame.pack(side='right')

        ##Bind the __patientSelect function to trigger when a patient is selected
        self.patientDisplay.bind('<<ListboxSelect>>', self.__patientSelect)
    
        
m=MainScreen("NICUAssigner")

if testing:
    m.addNurse("Frida", ['a', 'b', 'c'])
    m.addNurse("Franz", ['a', 'c'])
    m.addNurse("Fred", ['b', 'c'])
    
    m.addPatient("Claude", ['d', 'e', 'f'])

mainloop()
