from Blockchain.Blockchain import Blockchain
from FineChainAPI import API
from FineChainAPI.Session import Session

from pprint import pprint
import json

from tkinter import *
import tkinter.messagebox as tm

import pickle

class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)
        self.geometry('800x500')
        self.sessionid = None
        self.refreshid = None
        self.user_id = -1

    def switch_frame(self, frame_class, sessionid=None, user_id=-1, refreshid=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        if sessionid is not None:
            self.sessionid = sessionid
        if refreshid is not None:
            self.refreshid = refreshid
        if user_id > -1:
            self.user_id = user_id
        self._frame = new_frame
        self._frame.pack()

    def get_session_id(self):
        return self.sessionid

    def get_user_id(self):
        return self.user_id

    def get_refresh_id(self):
        return self.refreshid

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.username = ""
        self.password = ""
        self.user_id = -1

        self.sessionid = ""

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")
        self.label_title = Label(self) #could probably remove this and replace with padding

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_title.grid(row=0, column=1, sticky=E)
        self.label_username.grid(row=1, sticky=E)
        self.label_password.grid(row=2, sticky=E)
        self.entry_username.grid(row=1, column=1)
        self.entry_password.grid(row=2, column=1)

        #self.checkbox = Checkbutton(self, text="Keep me logged in")
        #self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)
        self.createusrbtn = Button(self, text="Create account", command=lambda: master.switch_frame(CreateAccountFrame, self.sessionid))
        self.createusrbtn.grid(columnspan=2)

        #self.mainbtn = Button(self, text="Main Screen", command=lambda: master.switch_frame(MainFrame))
        #self.mainbtn.grid(columnspan=2)

        self.pack()

    def authenticate_login(self, response):
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorLoginFrame)

        if response["message"] == "Successfully loged in":
            self.sessionid = response["body"]["session"]
            self.refreshid = response["body"]["refresh"]
            self.user_id = response["body"]["user_id"]
            self.master.switch_frame(MainFrame, self.sessionid, self.user_id, self.refreshid)
            self.master.switch_frame(MainFrame, self.sessionid, self.user_id, self.refreshid)
            #print(sessionid)
        else:
            self.master.switch_frame(ErrorLoginFrame)
            print(response)

        #if(str(response) == )
        #json_response = response.json()
        #print(json_response)

    def _login_btn_clicked(self):
        self.username = self.entry_username.get()
        self.password = self.entry_password.get()
        if self.username is not "" and self.password is not "":
            API.login(self.username,self.password).subscribe(on_next= lambda response: {
                self.authenticate_login(response)
            })
        else:
            self.master.switch_frame(ErrorLoginFrame)

        #response = API.login(username, password).subscribe(on_next= lambda response: {
        #    pprint(response)

        #})

        #display welcome in GUI if authenticated later

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        #print(master.get_session_id())
        #print("this is a test of sessionid")
        self.sessionid = master.get_session_id()
        self.user_id = master.get_user_id()
        self.name = self.set_name()
        self.refreshid = master.get_refresh_id()


        welcometext = "Welcome, %s" % (self.name)   #how the heck do i get a user's name from their session]
        self.label_welcome = Label(self, text=welcometext)
        self.createusrbtn = Button(self, text="Create account", command=lambda: master.switch_frame(CreateAccountMainFrame, self.sessionid, self.user_id, self.refreshid))
        self.createcompbtn = Button(self, text="Create company", command=lambda: master.switch_frame(CreateCompanyFrame, self.sessionid, self.user_id, self.refreshid))
        #self.updatecompbtn = Button(self, text="Update company", command=lambda: master.switch_frame(UpdateCompanyFrame, self.sessionid, self.user_id)) #add later
        self.usrtocompbtn = Button(self, text="Add/remove users to/from company", command=lambda: master.switch_frame(UsersToCompanyFrame, self.sessionid, self.user_id, self.refreshid))

        self.psttransaction = Button(self, text="Add transaction", command=lambda: master.switch_frame(PostTransactionFrame, self.sessionid, self.user_id, self.refreshid))

        self.logoffbtn = Button(self, text="logoff", command=self._logoff_btn_clicked)

        self.label_getcompany = Label(self, text="Print company information to console")
        self.entry_getcompany = Entry(self)
        self.printcompbtn = Button(self, text="Print", command=self.print_company)
        #self.logoffbtn.grid(columnspan=2)



        self.label_welcome.grid(row=0, column=2, sticky=E)
        self.createusrbtn.grid(row=1, column=0, sticky=E)
        self.createcompbtn.grid(row=2, column=0, sticky=E)
        #self.updatecompbtn.grid(row=3, column=0, sticky=E)
        self.usrtocompbtn.grid(row=4, column=0, sticky=E)
        self.psttransaction.grid(row=1, column=3, sticky=E)      #work on shifting these later
        self.logoffbtn.grid(row=2, column=3, sticky=E)
        self.label_getcompany.grid(row=8, column=2, sticky=E)
        self.entry_getcompany.grid(row=8, column=3, sticky=E)
        self.printcompbtn.grid(row=9,column=3,sticky=E)




        self.pack()

    def set_name(self):
        self.name = "this set_name doesn't work"
        API.getUser(self.user_id).subscribe(on_next= lambda response: {
            self.set_name_helper(response)
        })
        return self.name

    def set_name_helper(self, response):
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorLoginFrame)
        if response["message"] == "Default 404":
            print("User not found.")
        else:
            self.name = response["body"]["name"]


    def _logoff_btn_clicked(self):
        self.sessionid = None #delete the session
        #print(sessionid)
        self.master.switch_frame(LoginFrame)

    def print_company(self):
        self.companyid = self.entry_getcompany.get()
        self.tempsesh = Session()
        self.tempsesh.setSessionToken(self.sessionid)

        API.getCompany(self.companyid).subscribe(on_next=lambda response: {
            self.print_company_helper(response)
        })
        API.getCompanyFullchain(self.companyid,self.tempsesh).subscribe(on_next=lambda response: {
            self.print_companychain_helper(response)
        })

    def print_company_helper(self, response):
        print(response)

    def print_companychain_helper(self, response):
        chain = pickle.loads(response.content)
        pprint(vars(chain))


class ErrorLoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_error = Label(self, text="Encountered an error logging in. Please try again.")
        self.label_error.grid(columnspan=2)
        self.returnbtn = Button(self, text="Ok", command=lambda: master.switch_frame(LoginFrame))
        self.returnbtn.grid(columnspan=2)

        self.pack()

class CreateCompanyFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.sessionid = master.get_session_id()
        self.user_id = master.get_user_id()
        self.companyname = ""

        self.label_title = Label(self)

        self.label_name = Label(self, text="Company name")
        self.entry_name = Entry(self)

        self.label_title.grid(row=0,column=1,sticky=E)
        self.label_name.grid(row=1, sticky=E)
        self.entry_name.grid(row=1, column=2, sticky=E)

        self.submitappbtn = Button(self, text="Submit application", command=self.create_company)
        self.submitappbtn.grid(columnspan=2)
        self.returnbtn = Button(self, text="Return to home page", command=lambda: master.switch_frame(MainFrame))
        self.returnbtn.grid(columnspan=2)

        self.pack()

    def create_company(self):
        self.companyname = self.entry_name.get()
        self.tempsesh = Session()
        self.tempsesh.setSessionToken(self.sessionid)

        API.createCompany(self.companyname,self.tempsesh).subscribe(on_next=lambda response: {
            self.create_company_helper(response)
        })

    def create_company_helper(self, response):
        print(response)
        print("works")
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorCreateCompanyFrame)
        if response["message"] == "Successfully created new COMPANY":
            #self.master.switch_frame(MainFrame)
            #text = "Successfully created %s" % (response["body"]["username"])
            text = "Successfully created new company."
            self.label_createduser = Label(self, text=text)
        else:
            self.master.switch_frame(ErrorCreateCompanyFrame)


class UpdateCompanyFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

class UsersToCompanyFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.sessionid = master.get_session_id()
        self.user_id = master.get_user_id()
        self.companyid = -1
        self.user_id_to_mod = -1

        self.label_title = Label(self)

        self.label_name = Label(self, text="Username to add/remove")
        self.entry_name = Entry(self)
        self.label_name_id = Label(self, text="User id to add/remove")
        self.entry_name_id = Entry(self)
        self.label_companyid = Label(self, text="Company id")
        self.entry_companyid = Entry(self)

        self.label_title.grid(row=0,column=1,sticky=E)
        self.label_name.grid(row=1, sticky=E)
        self.entry_name.grid(row=1, column=2, sticky=E)
        self.label_name_id.grid(row=2, sticky=E)
        self.entry_name_id.grid(row=2, column=2, sticky=E)
        self.label_companyid.grid(row=3, sticky=E)
        self.entry_companyid.grid(row=3, column=2, sticky=E)

        self.addusrbtn = Button(self, text="Add user", command=self.add_user)
        self.addusrbtn.grid(row=4, columnspan=1)
        self.removeusrbtn = Button(self, text="Remove user", command=self.remove_user)
        self.removeusrbtn.grid(row=4, column=2, columnspan=1)
        self.returnbtn = Button(self, text="Return to home page", command=lambda: master.switch_frame(MainFrame, self.sessionid, self.user_id))
        self.returnbtn.grid(row=6, columnspan=2)

    def add_user(self):
        self.user_id_to_mod = self.entry_name_id.get()
        self.username = self.entry_name.get()
        self.companyid = self.entry_companyid.get()

        self.tempsesh = Session()
        self.tempsesh.setSessionToken(self.sessionid)

        self.tupleusers = (self.user_id_to_mod,self.username)
        self.users = [self.tupleusers]

        API.addUsersToCompany(self.companyid, self.users, self.tempsesh).subscribe(on_next=lambda response: {
            self.add_user_helper(response)
        })

        return
        #API.addUsersToCompany()

    def add_user_helper(self, response):
        print(response)
        #if str(response) == "<Response [500]>":
        #    self.master.switch_frame(ErrorCreateCompanyFrame)


    def remove_user(self):
        self.user_id_to_mod = self.entry_name_id.get()
        self.username = self.entry_name.get()
        self.companyid = self.entry_companyid.get()

        self.tempsesh = Session()
        self.tempsesh.setSessionToken(self.sessionid)

        self.tupleusers = (self.user_id_to_mod,self.username)
        self.users = [self.tupleusers]

        API.removeUsersFromCompany(self.companyid, self.users, self.tempsesh).subscribe(on_next=lambda response: {
            self.remove_user_helper(response)
        })

        return

    def remove_user_helper(self, response):
        print(response)

class PostTransactionFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.sessionid = master.get_session_id()
        self.user_id = master.get_user_id()
        self.refreshid = master.get_refresh_id()
        self.companyid = -1
        self.amount = -1
        self.to = ""
        self.recipient = ""

        self.label_title = Label(self)

        self.label_companyid = Label(self, text="Company id:")
        self.entry_companyid = Entry(self)
        self.label_to = Label(self, text="To: ")
        self.entry_to= Entry(self)
        self.label_from = Label(self, text="From: ")
        self.entry_from = Entry(self)
        self.label_amount = Label(self, text="Amount: ")
        self.entry_amount = Entry(self)

        self.label_title.grid(row=0,column=1,sticky=E)
        self.label_companyid.grid(row=1, sticky=E)
        self.entry_companyid.grid(row=1, column=2, sticky=E)
        self.label_to.grid(row=2, sticky=E)
        self.entry_to.grid(row=2, column=2, sticky=E)
        self.label_from.grid(row=3, sticky=E)
        self.entry_from.grid(row=3, column=2, sticky=E)
        self.label_amount.grid(row=4, sticky=E)
        self.entry_amount.grid(row=4, column=2, sticky=E)

        self.addusrbtn = Button(self, text="Add transaction", command=self.add_transaction)
        self.addusrbtn.grid(row=5, column=2, columnspan=1)
        self.returnbtn = Button(self, text="Return to home page", command=lambda: master.switch_frame(MainFrame, self.sessionid, self.user_id))
        self.returnbtn.grid(row=8, column=2, columnspan=2)

    def add_transaction(self):
        self.companyid = self.entry_companyid.get()
        self.amount = self.entry_amount.get()
        self.to = self.entry_to.get()
        self.recipient = self.entry_from.get()

        self.tempsesh = Session()
        self.tempsesh.setSessionToken(self.sessionid)
        self.tempsesh.setRefreshToken(self.refreshid)

        API.postTransaction(self.companyid, self.to, self.recipient, self.amount, self.tempsesh).subscribe(on_next=lambda response: {
            self.add_transaction_helper(response)
        })
        return

    def add_transaction_helper(self, response):
        print(response)


class CreateAccountFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_title = Label(self)

        self.label_name = Label(self, text="Name")
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")
        self.label_email = Label(self, text="Email")


        self.entry_name = Entry(self)
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")
        self.entry_email = Entry(self)      #add regex later?

        self.label_title.grid(row=0, column=1, sticky=E)
        self.label_name.grid(row=1, sticky=E)
        self.label_username.grid(row=2, sticky=E)
        self.label_password.grid(row=3, sticky=E)
        self.label_email.grid(row=4, sticky=E)
        self.entry_name.grid(row=1, column=1)
        self.entry_username.grid(row=2, column=1)
        self.entry_password.grid(row=3, column=1)
        self.entry_email.grid(row=4, column=1)

        self.submitappbtn = Button(self, text="Submit application", command=self.create_user)
        self.submitappbtn.grid(columnspan=2)
        self.returnbtn = Button(self, text="Return to login", command=lambda: master.switch_frame(LoginFrame))
        self.returnbtn.grid(columnspan=2)

        self.pack()

    def create_user(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()

        API.createUser(name,username,password,email).subscribe(on_next=lambda response: {
            self.create_user_helper(response)
        })

    def create_user_helper(self, response):
        print(response)
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorCreateAccountFrame)
        if response["message"] == "Successfully created new USER":
            #self.master.switch_frame(MainFrame)
            #text = "Successfully created %s" % (response["body"]["username"])
            text = "Successfully created new user."
            self.label_createduser = Label(self, text=text)
            self.label_createduser.grid(row=5, column=1)
            self.submitappbtn.destroy()
        else:
            self.master.switch_frame(ErrorCreateAccountFrame)

class CreateAccountMainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_title = Label(self)

        self.label_name = Label(self, text="Name")
        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")
        self.label_email = Label(self, text="Email")


        self.entry_name = Entry(self)
        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")
        self.entry_email = Entry(self)      #add regex later?

        self.label_title.grid(row=0, column=1, sticky=E)
        self.label_name.grid(row=1, sticky=E)
        self.label_username.grid(row=2, sticky=E)
        self.label_password.grid(row=3, sticky=E)
        self.label_email.grid(row=4, sticky=E)
        self.entry_name.grid(row=1, column=1)
        self.entry_username.grid(row=2, column=1)
        self.entry_password.grid(row=3, column=1)
        self.entry_email.grid(row=4, column=1)

        self.submitappbtn = Button(self, text="Submit application", command=self.create_user)
        self.submitappbtn.grid(columnspan=2)
        self.returnbtn = Button(self, text="Return to home page", command=lambda: master.switch_frame(MainFrame))
        self.returnbtn.grid(columnspan=2)

        self.pack()

    def create_user(self):
        name = self.entry_name.get()
        username = self.entry_username.get()
        password = self.entry_password.get()
        email = self.entry_email.get()

        API.createUser(name,username,password,email).subscribe(on_next=lambda response: {
            self.create_user_helper(response)
        })

    def create_user_helper(self, response):
        print(response)
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorCreateAccountFrame)
        if response["message"] == "Successfully created new USER":
            #self.master.switch_frame(MainFrame)
            #text = "Successfully created %s" % (response["body"]["username"])
            text = "Successfully created new user."
            self.label_createduser = Label(self, text=text)
            self.label_createduser.grid(row=5, column=1)
            self.submitappbtn.destroy()
        else:
            self.master.switch_frame(ErrorCreateAccountFrame)

class ErrorCreateAccountFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_error = Label(self, text="Encountered an error creating an account. Please try again.")
        self.label_error.grid(columnspan=2)
        self.returnbtn = Button(self, text="Ok", command=lambda: master.switch_frame(CreateAccountFrame))
        self.returnbtn.grid(columnspan=2)

        self.pack()



if __name__ == '__main__':
    app = MainApp()
    app.title("FineChain")
    #app['SESSION'] = Session()
    #app['SESSION'] . setsessiontokenthing()
    #lf = LoginFrame(app)
    #app.geometry('500x300')
    app.mainloop()
