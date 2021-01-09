from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import scrolledtext
from nurse import *
from attributes import *
from patient import *
import sys, os

testing = True

class MainScreen:
    
    def __init__(self, name):
        ##Create a base window everything is built on
        self.tk = Tk(screenName=name, baseName=name)
        self.tk.title(name)
        if getattr(sys, 'frozen', False):
            applicationPath = sys._MEIPASS
        elif __file__:
            applicationPath = os.path.dirname(__file__)
        self.tk.iconbitmap(os.path.join(applicationPath, 'rafal.ico'))

        ##Create variables to store lists of nurses and patients
        self.nurses = []
        self.patients = []

        ##Create variables to store possible attributes of nurses and patients
        self.nurseAttrs = []
        self.patientAttrs = []
        self.attrRelations = {}

        ##Create display for nurse names and attributes
        self.nurseFrame = Frame(self.tk)
        self.nurseDisplay = Listbox(self.nurseFrame, width=30)
        self.nurseAttrsDisplay = []
        self.nurseCheckVars = []
        self.nurseAttrsFrame = Frame(self.nurseFrame)
        ##Create buttons to modify nurses
        self.addNurseBtn = Button(self.nurseFrame, text="Add Nurse")
        self.editNurseBtn = Button(self.nurseFrame, text="Edit Nurse")
        self.removeNurseBtn = Button(self.nurseFrame, text="Remove Nurse")

        ##Create display for patient names and attributes
        self.patientFrame = Frame(self.tk)
        self.patientDisplay = Listbox(self.patientFrame, width=30)
        self.patientAttrsDisplay = []
        self.patientCheckVars = []
        self.patientAttrsFrame = Frame(self.patientFrame)
        ##Create buttons to modify patients
        self.addPatientBtn = Button(self.patientFrame, text="Add Patient")
        self.editPatientBtn = Button(self.patientFrame, text="Edit Patient")
        self.removePatientBtn = Button(self.patientFrame, text="Remove Patient")

        ##Create frame for information display
        self.dataFrame = Frame(self.tk)
        self.infoText = scrolledtext.ScrolledText(self.dataFrame, wrap="word", width=30)
        self.infoText.insert(END, "This box will be filled with information about nurses, patients, and attributes when selected")
        self.infoText.config(state='disabled')
        ##Create buttons to modify attributes
        self.addAttrBtn = Button(self.dataFrame, text="Add Attribute")
        self.editAttrBtn = Button(self.dataFrame, text="Edit Attribute")
        self.removeAttrBtn = Button(self.dataFrame, text="Remove Attribute")

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
                self.attrRelations[a] = []

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
                self.__nurseSelect(0)

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
                
                c.grid(row=nA, column=0, sticky='w')
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

        ##TODO: Update info text
        if len(index) > 0:
            self.infoText.config(state='normal')
            self.infoText.delete(1.0, END)
            toDisp = "Nurse "+name+":\n"
            toDisp += "Is currently treating the patients:\n"
            for i in nurse.getPatients():
                toDisp += i.getName()
                if nurse.getPatients().index(i) < len(nurse.getPatients())-1:
                    toDisp+=', '
            toDisp += "\nHas the attributes:\n"+', '.join(nurse.getAttrs())
            toDisp += "\n\nCan treat patients with the attributes:\n"
            canTreat = []
            for i in nurse.getAttrs():
                for j in self.attrRelations[i]:
                    if j not in canTreat:
                        canTreat.append(j)
            toDisp += ', '.join(canTreat)
            self.infoText.insert(1.0, toDisp)
            self.infoText.config(state='disabled')

                            
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

    def removePatient(self, patient):
        self.patients.remove(self.getPatient(patient))

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
                c=Checkbutton(self.patientAttrsFrame, text=a, variable=v, state='disabled', command=self.__patientCheckBtn)
                self.patientCheckVars.append(v)
                c.grid(row=self.patientAttrs.index(a), column=0, sticky='w')
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

        ##TODO: Update info text
        if len(index) > 0:
            self.infoText.config(state='normal')
            self.infoText.delete(1.0, END)
            self.infoText.insert(1.0, "TODO: Populate with info about "+name)
            self.infoText.config(state='disabled')

    def __addPatientBtn(self):
        """Button event to add a patient"""
        name= simpledialog.askstring("Patient name", "What is the patient's name?")
        if name:
            self.addPatient(name, [])
            self.patientDisplay.focus()
            self.patientDisplay.selection_clear(0, END)
            self.patientDisplay.selection_set(self.patients.index(self.getPatient(name)))
            self.patientDisplay.activate(self.patients.index(self.getPatient(name)))
            print(self.patients.index(self.getPatient(name)))
            print(self.patientDisplay.curselection())
            self.__patientSelect(0)
            self.__editPatientBtn(fromAdd=True)

    def __editPatientBtn(self, fromAdd=False):

        toggle = self.editPatientBtn.cget('text')

        print(toggle)
        if toggle == 'Edit Patient':
            self.editPatientBtn.config(text='Finished Editing')
            for b in self.patientAttrsDisplay:
                b.config(state='active')

        elif not fromAdd:
            self.editPatientBtn.config(text='Edit Patient')
            for b in self.patientAttrsDisplay:
                b.config(state='disabled')

    def __removePatientBtn(self):
        
        w = self.patientDisplay
        index = w.curselection()

        name = w.get(index)
        self.removePatient(name)

    def __patientCheckBtn(self):
        
        ##Get selected patient
        w = self.patientDisplay
        index = w.curselection()

        name = w.get(index)
        patient = self.getPatient(name)
        
        selAttr = []
        for b in self.patientAttrsDisplay:
            bVar = b.cget('var')
            isSelected = self.tk.getint(self.tk.getvar(bVar))

            if isSelected != 0:
                if b.cget('text') not in patient.getAttrs():
                    patient.addAttr(b.cget('text'))

            if isSelected == 0:
                if b.cget('text') in patient.getAttrs():
                    patient.removeAttr(b.cget('text'))

    def createNewAttr(self, np, name, related, window=0):
        print(name, np, np==0, np==1)
        if name != '':
            if np == 0:
                
                if name not in self.nurseAttrs:
                    self.nurseAttrs.append(name)
                    self.attrRelations[name] = []

                if related != '':
                    relList = related.split(', ')
                    for i in relList:
                        if i not in self.patientAttrs:
                            self.patientAttrs.append(i)
                        if i not in self.attrRelations[name]:
                            self.attrRelations[name].append(i)
                
            elif np == 1:
                
                if name not in self.patientAttrs:
                    self.patientAttrs.append(name)

                if related != '':
                    relList = related.split(', ')
                    for i in relList:
                        if i not in self.nurseAttrs:
                            self.nurseAttrs.append(name)
                            self.attrRelations[i] = [name]
                        if name not in self.attrRelations[i]:
                            self.attrRelations[i].append(name)

        self.updateNurses()
        self.updatePatients()
        if window != 0:
            window.destroy()
                    
    def __addAttrBtn(self):
        attrWindow = Tk()
        attrWindow.title("New Attribute Entry")
        q1 = Label(attrWindow, text="Please enter the attribute's name")
        q1.pack(side='top')
        attrName = Entry(attrWindow)
        attrName.pack(side='top')

        nursePatientLabel = Label(attrWindow, text="Is this a nurse attribute \nor a patient attribute?")
        nursePatientLabel.pack(side='top')

        radioFrame = Frame(attrWindow)
        radioVar = IntVar()
        nurseRadio = Radiobutton(radioFrame, text="Nurse", variable=radioVar, value=0)
        patientRadio = Radiobutton(radioFrame, text="Patient", variable=radioVar, value=1)
        nurseRadio.pack(side='left')
        patientRadio.pack(side='right')
        nurseRadio.select()
        radioFrame.pack(side='top')

        relativeLabel = Label(attrWindow, text="Is there a related attribute to \nassociate this attribute with?\nEnter in a comma separated list")
        relativeLabel.pack(side='top')

        assocAttrs = Entry(attrWindow)
        assocAttrs.pack(side='top', fill='both')

        confirmAdd = Button(attrWindow, text="Create Attribute", command=lambda: self.createNewAttr(
            radioVar.get(), attrName.get(), assocAttrs.get(), attrWindow))
        confirmAdd.pack(side='bottom', fill='both')

    def __editAttrBtn(self):
        attrWindow = Tk()
        #attrWindow.attributes('-topmost', True)
        attrWindow.title("Edit Attribute")
        q1 = Label(attrWindow, text="Select Attribute to Edit")
        q1.pack(side='top', fill='both')

        allAttrs = []
        btnFrame = Frame(attrWindow)
        nurseVars = []
        patientVars = []

        def checkCommand():
            n = selected.get()
            if 'Patient' in n:
                name = n.replace(' (Patient)', '')
                for bNum in range(0, len(nurseBtns)):
                    b = nurseBtns[bNum]
                    isSelected = nurseVars[bNum].get()
                        
                    if isSelected == 1:
                        nurseAttrName = b.cget('text')
                        if name not in self.attrRelations[nurseAttrName]:
                            self.attrRelations[nurseAttrName].append(name)
                    else:
                        nurseAttrName = b.cget('text')
                        if name in self.attrRelations[nurseAttrName]:
                            self.attrRelations[nurseAttrName].remove(name)

            else:
                name = n.replace(' (Nurse)', '')
                for bNum in range(0, len(patientBtns)):
                    b = patientBtns[bNum]
                    isSelected = patientVars[bNum].get()
                        
                    if isSelected == 1:
                        patientAttrName = b.cget('text')
                        if patientAttrName not in self.attrRelations[name]:
                            self.attrRelations[name].append(patientAttrName)
                    else:
                        patientAttrName = b.cget('text')
                        if patientAttrName in self.attrRelations[name]:
                            self.attrRelations[name].remove(patientAttrName) 

        nurseBtns = []
        for a in self.nurseAttrs:
            allAttrs.append(a+" (Nurse)")
            i = IntVar(btnFrame)
            i.initialize(0)
            nurseVars.append(i)
            nurseBtns.append(Checkbutton(btnFrame, text=a, variable=nurseVars[-1], command=checkCommand))
            
            
        patientBtns = []
        for a in self.patientAttrs:
            allAttrs.append(a+" (Patient)")
            i = IntVar(btnFrame)
            i.initialize(0)
            patientBtns.append(Checkbutton(btnFrame, text=a, variable=i, command=checkCommand))                
            patientVars.append(i)

        def valSelect(event):
            if 'Patient' in event:
                attrName = event.replace(' (Patient)', '')
                for b in nurseBtns:
                    b.grid(row=nurseBtns.index(b), column=0, sticky="W")
                    if attrName in b.cget('text'):
                        b.select()
                for b in patientBtns:
                    b.grid_remove()

            else:
                for b in patientBtns:
                    b.grid(row=patientBtns.index(b), column=0, sticky="W")
                for b in nurseBtns:
                    b.grid_remove()
            
        selected = StringVar(attrWindow, value=allAttrs[0])
        toEdit = OptionMenu(attrWindow, selected, *allAttrs, command=valSelect)
        toEdit.pack(side="top", fill='x')

        descLabel = Label(attrWindow, text="This attribute is associated with the following attributes")
        descLabel.pack(side='top')
        btnFrame.pack(side="top")

        def confirm():
            yn = messagebox.askquestion(master=attrWindow, title="Confirm changes?", message="Confirm attribute changes?")
            print(yn)
            if yn == "yes":
                attrWindow.destroy()
            else:
                attrWindow.focus()

            self.updateNurses()
            self.updatePatients()
            self.__nurseSelect(0)
            self.__patientSelect(0)
                
        confirmBtn = Button(attrWindow, text="Confirm changes", command=confirm)
        confirmBtn.pack(side="bottom")
        

    def __removeAttrBtn(self):
        attrWindow = Tk()
        attrWindow.title("Remove Attribute")
        q1 = Label(attrWindow, text="Select Attribute to Remove")
        q1.pack(side='top', fill='both')

        allAttrs = []
        for a in self.nurseAttrs:
            allAttrs.append(a+" (Nurse)")

        for a in self.patientAttrs:
            allAttrs.append(a+" (Patient)")

        selected = StringVar(attrWindow, value=allAttrs[0])
        toRemove = OptionMenu(attrWindow, selected, *allAttrs)
        toRemove.pack(side="top", fill='x')

        

    def pack(self):
        """Puts all created objects on the main screen"""
        ##Create text saying "Nurses:" to label the nurses section of the widget
        self.nurseLabel = Label(self.nurseFrame, text="Nurses:")
        self.nurseLabel.pack(side='top')
        
        ##Add nurse buttons to bottom of the display in reverse order
        self.removeNurseBtn.pack(side='bottom', fill='both')
        self.editNurseBtn.pack(side='bottom', fill='both')
        self.addNurseBtn.pack(side='bottom', fill='both')
        self.addNurseBtn.config(command=self.__addNurseBtn)
        self.editNurseBtn.config(command=self.__editNurseBtn)
        self.removeNurseBtn.config(command=self.__removeNurseBtn)
        
        ##Add the nurse list to the display on the left
        self.nurseDisplay.pack(side='left', fill='both', expand=True)
        
        ##Add frame with checkbuttons on the right
        self.nurseAttrsFrame.pack(side='right', fill='both')
        
        ##Add frame with all nurse data on the left of the main widget
        self.nurseFrame.pack(side='left', fill='y')
        
        ##Bind the __nurseSelect function to trigger when a nurse is selected
        self.nurseDisplay.bind('<<ListboxSelect>>', self.__nurseSelect)


        ##Create text saying "Patients:" to label the patients section of the widget
        self.patientLabel = Label(self.patientFrame, text="Patients:")
        self.patientLabel.pack(side='top')
        
        ##Add patient buttons in reverse order
        self.removePatientBtn.pack(side='bottom', fill='both')
        self.editPatientBtn.pack(side='bottom', fill='both')
        self.addPatientBtn.pack(side='bottom', fill='both')
        self.addPatientBtn.config(command=self.__addPatientBtn)
        self.editPatientBtn.config(command=self.__editPatientBtn)
        self.removePatientBtn.config(command=self.__removePatientBtn)
        
        ##Add the patient list to the right of the frame
        self.patientDisplay.pack(side='right', fill='both')
        
        ##Add the button frame to the left of the frame
        self.patientAttrsFrame.pack(side='left', fill='both')

        ##Add the patient frame on the right of the main screen
        self.patientFrame.pack(side='right', fill='both')

        ##Bind the __patientSelect function to trigger when a patient is selected
        self.patientDisplay.bind('<<ListboxSelect>>', self.__patientSelect)

        ##Add data frame to the center of the screen
        self.dataFrame.pack(side='left', fill='both', expand=True)

        ##Assign buttons and text box to locations in the data frame
        self.removeAttrBtn.pack(side='bottom', fill='x')
        self.editAttrBtn.pack(side='bottom', fill='x')
        self.addAttrBtn.pack(side='bottom', fill='x')
        self.infoText.pack(side='bottom', fill='both', expand=True)
        self.addAttrBtn.config(command=self.__addAttrBtn)
        self.editAttrBtn.config(command=self.__editAttrBtn)
        self.removeAttrBtn.config(command=self.__removeAttrBtn)
    
        
m=MainScreen("NICUAssigner")

if testing:
    m.addNurse("Frida", ['obdormition', 'borborgymus', 'xerosis'])
    m.addNurse("Franz", ['borborgymus', 'xerosis'])
    m.addNurse("Fred", ['obdormition'])
    
    m.addPatient("Claude", ['sphenopalatine ganglioneuralgia', 'morsicatio buccarum', 'lachrymation'])
    m.addPatient("Carl", ['morsicatio buccarum', 'lachrymation'])

mainloop()
