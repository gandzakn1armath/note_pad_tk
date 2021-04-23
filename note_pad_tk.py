import threading
import datetime
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type
from tkinter import *
from firebase import firebase
import json

firebase = firebase.FirebaseApplication("https://pythonnotepad-default-rtdb.firebaseio.com/", None)

#/////////////////////////////////////////////////////////

class RegistrationDialog:
    def __init__(self):
        self.signUpDialog = Tk()
        self.signUpDialog.title("Գրանցվել")
        tkWidth = 250
        tkHeight = 350
        pcWidth = 1366
        pcHeight = 768
        self.signUpDialog.geometry(
            str(tkWidth) + "x" + str(tkHeight) + "+" + str(int((pcWidth - tkWidth) / 2)) + "+" + str(
                int((pcHeight - tkHeight) / 2)))

        Label(self.signUpDialog, text="Անուն").place(x=100, y=0)
        self.firstName = StringVar()
        self.firstNameLabel = Entry(self.signUpDialog, textvariable=self.firstName).place(x=60, y=20)
        Label(self.signUpDialog, text="Ազգանուն").place(x=90, y=60)
        self.lastName = StringVar()
        self.lastNameLabel = Entry(self.signUpDialog, textvariable=self.lastName).place(x=60, y=80)
        Label(self.signUpDialog, text="Հեռախոսահամար").place(x=70, y=120)
        self.phoneNumber = StringVar()
        self.phoneNumberLabel = Entry(self.signUpDialog, textvariable=self.phoneNumber).place(x=60, y=140)
        Label(self.signUpDialog, text="Գաղտնաբառ").place(x=80, y=180)
        self.password = StringVar()
        self.passwordLabel = Entry(self.signUpDialog, textvariable=self.password).place(x=60, y=200)
        self.signUpDialog.resizable(False, False)

    def getFirstName(self):
        return str(self.firstName.get())

    def getLastName(self):
        return str(self.lastName.get())

    def getPhoneNumber(self):
        self.phoneNumber.get()
        return str(self.phoneNumber.get())

    def getPassword(self):
        return str(self.password.get())

    def show(self, signUp, signIn):
        Button(self.signUpDialog, text="Գրանցվել", command=signUp).place(x=90, y=260)
        Button(self.signUpDialog, text="Մուտք գործել", command=signIn).place(x=80, y=300)
        self.signUpDialog.mainloop()

    def hide(self):
        self.signUpDialog.destroy()

    def showFirstNameError(self):
        self.firstNameError = Label(self.signUpDialog, text="Մուտքագրել ձեր անուն", fg='red')
        self.firstNameError.place(x=55, y=40)

    def showLastNameError(self):
        self.lastNameError = Label(self.signUpDialog, text="Մուտքագրել ձեր ազգանունը", fg='red').place(x=45, y=100)

    def showPhoneNumberError(self):
        self.phoneNumberError = Label(self.signUpDialog, text="Մուտքագրել ձեր հեռախոսահամարը", fg='red').place(x=20,
                                                                                                               y=160)

    def showPasswordError(self):
        self.passwordError = Label(self.signUpDialog, text="Մուտքագրել 6 նիշից ավել", fg='red').place(x=50, y=220)

    def hideErrorFirstName(self):
        try:
            self.firstNameError.destroy()
        except:
            pass

    def hideErrorLastName(self):
        try:
            self.lastNameError.destroy()
        except:
            pass

    def hideErrorPhoneNumber(self):
        try:
            self.phoneNumberError.destroy()
        except:
            pass

    def hideErrorPassword(self):
        try:
            self.passwordError.destroy()
        except:
            pass

#/////////////////////////////////////////////////////////

class SigninDialog():
    def __init__(self):
        self.signinDialog = Tk()
        self.signinDialog.title("Մուտք գործել")
        tkWidth = 180
        tkHeight = 230
        pcWidth = 1366
        pcHeight = 768
        self.signinDialog.geometry(
            str(tkWidth) + "x" + str(tkHeight) + "+" + str(
                int((pcWidth - tkWidth) / 2)) + "+" + str(
                int((pcHeight - tkHeight) / 2)))
        Label(self.signinDialog, text="Մուտքանուն").pack()
        self.phoneNumber = StringVar()
        Entry(self.signinDialog, textvariable=self.phoneNumber).pack()

        Label(self.signinDialog, text="Գաղտնաբառ").pack()
        self.password = StringVar()
        Entry(self.signinDialog, textvariable=self.password).pack()

    def get_login(self):
        return str(self.phoneNumber.get())

    def get_password(self):
        return str(self.password.get())


    def show(self, signIn, signUp):
        Button(self.signinDialog, text="Մուտք գործել", command=signIn).pack()
        Button(self.signinDialog, text="Գրանցվել", command=signUp).pack()
        self.signinDialog.resizable(False, False)
        self.signinDialog.mainloop()



    def hide(self):  # փակում է պատուհանը
        self.signinDialog.destroy()

#/////////////////////////////////////////////////////////

class Note:
    def __init__(self, notes):
        self.user = open("userInfo.txt", "r")
        self.userId = json.load(self.user)
        self.notes = notes
        self.currentDate = datetime.datetime.now()

    def data(self):
        return {
            'createAt': self.currentDate,
            'not': self.notes,
            'user_id': self.userId["id"]
        }

#/////////////////////////////////////////////////////////

class User:

    def setFirstName(self, firstname):
        if not firstname.strip().replace(" ", "").isalpha():
            return False
        self.firstName = firstname
        return True

    def setLastName(self, lastname):
        if not lastname.strip().replace(" ", "").isalpha():
            return False
        self.lastName = lastname
        return True

    def hasPhoneNumber(self, phoneNumber, user_data):
        try:
            sym = str(phoneNumber)
            if sym[0] == "0":
                phoneNumber = "+374" + sym[1:]
            for r in user_data:
                res = user_data[r]
                if str(res["phoneNumber"]) == phoneNumber:
                    return True
            return False
        except:
            return False

    def setPhoneNumber(self, phoneNumber):
        try:
            sym = str(phoneNumber)
            if sym[0] == "0":
                phoneNumber = "+374" + sym[1:]

            s = carrier._is_mobile(number_type(phonenumbers.parse(phoneNumber)))
            self.phoneNumber = phoneNumber
            return True
        except:
            return False

    def setPassword(self, password):
        if not password.strip().replace(" ", "") or len(password) <= 5:
            return False
        self.password = password
        return True

    def getData(self):
        return {
            'firstName': self.firstName,
            'lastName': self.lastName,
            'phoneNumber': self.phoneNumber,
            'password': self.password,
        }

#/////////////////////////////////////////////////////////

class MainMenu:
    def __init__(self):
        self.inputFile = "userInfo.txt"
        self.notes = []
        self.notesId = []
        self.myfile = open(self.inputFile, mode='r')
        self.userInfo = json.load(self.myfile)
        self.firstName = self.userInfo["firstName"]
        self.lastName = self.userInfo["lastName"]
        self.name = str(self.firstName + " " + self.lastName)

        self.master = Tk()
        self.isEdit = False
        self.left = Frame(self.master, width=900, height=500, bg='white').pack(side=LEFT)
        self.master.geometry("900x500")
        self.master.resizable(False, False)
        Label(self.left, text=self.name, font=('georgia 8 bold'), fg='black', bg='white').place(x=10, y=2)
        Label(self.left, text="Գրառումներ", font=('georgia 10 bold'), fg='black', bg='white').place(x=460, y=0)
        # ստեղծում է գծային հատվածը
        Frame(self.master, width=5, height=500, bg='black').place(x=450, y=0)
        Frame(self.master, width=1000, height=5, bg='black').place(x=0, y=0)
        Frame(self.master, width=1000, height=5, bg='black').place(x=0, y=20)
        Frame(self.master, width=1000, height=5, bg='black').place(x=0, y=495)
        self.listbox = Listbox(self.master, exportselection=0, width=70, height=28, bg='gray')
        self.listbox.place(x=465, y=30)
        # ստեղծում է գրառումների ցուցակ
        self.inputLabel = Text(self.left, width=50, height=16, bg='gray')
        self.inputLabel.place(x=10, y=30)
        self.btn_text = StringVar()

    def setUpNotes(self, listArray):
        print(listArray)
        index = 0
        for item in listArray:
            self.listbox.insert(index, str(item))
            index += 1

    def get_current_select(self):
        selectItem = self.listbox.curselection()
        return selectItem[0]

    def insertAnchor(self):
        self.selectItem = self.listbox.curselection()
        if self.selectItem:
            if self.isEdit:
                select_index = self.selectItem[0]
                # save note
                self.user = open("userInfo.txt", "r")
                self.userId = json.load(self.user)

                self.isEdit = False
                self.btn_text.set("Փոփոխել")
                inputText = self.inputLabel.get(1.0, END + "-1c")
                note = Note(inputText)
                firebase.put('connectpythonf/Note', self.notesId[select_index], note.data())
                self.listbox.delete(ACTIVE)
                self.listbox.insert(select_index, inputText)
                self.inputLabel.delete(1.0, 'end')
            else:
                self.isEdit = True
                self.btn_text.set("Պահպանել")
                s = self.listbox.get(ANCHOR)
                self.inputLabel.delete(1.0, 'end')
                self.inputLabel.insert(1.0, s)

            # selectItem = int(selectItem) + 1
        else:
            print("Null")

    def insertText(self):
        m = self.inputLabel.get(1.0, END + "-1c")
        if m:
            self.inputLabel.delete(1.0, 'end')
            self.note = Note(m)
            self.result = firebase.post('connectpythonf/Note', self.note.data())
            self.listbox.insert(END, m)
            self.notesId.append(self.result["name"])
            self.notes.append(m)

        else:
            print("Null")

    def delet_note(self, index):
        self.listbox.delete(index)

    def insert_not(self):
        self.myfile = open("userInfo.txt", 'r')
        self.user = json.load(self.myfile)
        self.userId = self.user["id"]
        note_data = firebase.get('connectpythonf/Note', None)
        if not note_data:
            return

        self.notes = []
        self.notesId = []
        for noteId in note_data:
            note = note_data[noteId]
            user_id = note["user_id"]
            if self.userId == user_id:
                note = note["not"]
                self.notesId.append(noteId)
                self.notes.append(note)
        self.setUpNotes(self.notes)

    def show(self, delete, exit):
        self.insert_not()
        self.btn_text.set("Փոփոխել")
        Button(self.left, textvariable=self.btn_text, width=16, height=2, bg='black', fg='white',
               command=self.insertAnchor).place(x=150, y=320)
        Button(self.left, text="Ստեղծել", width=16, height=2, fg='white', bg='black', command=self.insertText).place(
            x=10, y=320)

        Button(self.left, text="Ջնջել", width=16, height=2, fg='white', bg='black', command=delete).place(
            x=290, y=320)

        Button(self.left, text="Դուրս գալ հաշվից", width=56, height=2, bg='black', fg='white', command=exit).place(x=10, y=380)
        self.master.mainloop()

    def hide(self):
        self.master.destroy()

#/////////////////////////////////////////////////////////

sign_in: SigninDialog
reg: RegistrationDialog
user: User
menu: MainMenu


def saveData():
    global user
    result = firebase.post('connectpythonf/User', user.getData())
    res = result["name"]
    userInfo = open("userInfo.txt", "w")
    obj = json.dumps({"id": res,
                      "phoneNumber": user.phoneNumber,
                      "password": user.password,
                      "firstName": user.firstName,
                      "lastName": user.lastName})

    userInfo.write(obj)
    userInfo.close()
    print(result)
    show_menu()


def signIn():
    sign_in_result = firebase.get('connectpythonf/User', None)
    for d in sign_in_result:
        res = sign_in_result[d]
        login = str(sign_in.get_login())
        if login[0] == "0":
            login = "+374" + login[1:]
        if str(res["phoneNumber"]) == login and str(res["password"]) == sign_in.get_password():
            sign_in.hide()
            userInfo = open("userInfo.txt", "w")
            obj = json.dumps({"id": d,
                              "phoneNumber": res["phoneNumber"],
                              "password": res["password"],
                              "firstName": res["firstName"],
                              "lastName": res["lastName"]})

            userInfo.write(obj)
            userInfo.close()
            show_menu()
            break


def signUp():
    global reg, user
    user = User()
    if not user.setFirstName(reg.getFirstName()):
        reg.showFirstNameError()
        return
    reg.hideErrorFirstName()

    if not user.setLastName(reg.getLastName()):
        reg.showLastNameError()
        return
    reg.hideErrorLastName()

    if user.hasPhoneNumber(reg.getPhoneNumber(), firebase.get('connectpythonf/User', None)):
        reg.showPhoneNumberError()
        return
    reg.hideErrorPhoneNumber()

    if not user.setPhoneNumber(reg.getPhoneNumber()):
        reg.showPhoneNumberError()
        return
    reg.hideErrorPhoneNumber()

    if not user.setPassword(reg.getPassword()):
        reg.showPasswordError()
        return
    reg.hideErrorPassword()

    saveDataThread = threading.Thread(target=saveData)
    saveDataThread.start()
    reg.hide()


def show_sign_up_dialog():
    sign_in.hide()
    global reg
    reg = RegistrationDialog()
    reg.show(signUp, show_sign_in_dialog)


def show_sign_in_dialog():
    try:
        reg.hide()
    except:
        pass
    global sign_in
    sign_in = SigninDialog()
    sign_in.show(signIn, show_sign_up_dialog)


def delete():
    index = menu.get_current_select()
    firebase.delete('connectpythonf/Note', menu.notesId[index])
    menu.delet_note(index)


def exit():
    userInfo = open("userInfo.txt", "w")
    userInfo.write("")
    userInfo.close()
    menu.hide()
    show_sign_in_dialog()


def show_menu():
    global menu
    menu = MainMenu()
    menu.show(delete, exit)


try:
    user = open("userInfo.txt", "r")
    line = user.readlines()
    if line:
        show_menu()
    else:
        show_sign_in_dialog()
except:
    show_sign_in_dialog()

