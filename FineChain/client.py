from Blockchain.Blockchain import Blockchain
from FineChainAPI import API
from FineChainAPI.Session import Session

from pprint import pprint
import json

from tkinter import *
import tkinter.messagebox as tm

sessionid = None

class MainApp(Tk):

    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)
        self.geometry('500x300')
        self.sessionid = None

    def switch_frame(self, frame_class, sessionid=None):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()
        if sessionid is not None:
            self.sessionid = sessionid
            print("switch_frame works")

    def get_session_id(self):
        print(self.sessionid)
        print("the get function works")
        return self.sessionid
    #def set_session_id(self, sessionid):
    #    self.sessionid = sessionid

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.username = ""
        self.password = ""

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
        seshid = "sessionid %s" % (self.sessionid)
        print(seshid)
        self.createusrbtn.grid(columnspan=2)

        #self.mainbtn = Button(self, text="Main Screen", command=lambda: master.switch_frame(MainFrame))
        #self.mainbtn.grid(columnspan=2)

        self.pack()

    def authenticate_login(self, response):
        #print(response)
        if str(response) == "<Response [500]>":
            self.master.switch_frame(ErrorLoginFrame)

        if response["message"] == "Successfully loged in":
            self.sessionid = response["body"]["session"]
            self.master.switch_frame(MainFrame, self.sessionid)
            print(self.sessionid)
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

        welcometext = "Welcome, %s" % (self.sessionid)   #how the heck do i get a user's name from their session]
        self.label_welcome = Label(self, text=welcometext)
        self.createusrbtn = Button(self, text="Create account", command=lambda: master.switch_frame(CreateAccountFrame))
        self.createcompbtn = Button(self, text="Create company", command=lambda: master.switch_frame(CreateCompanyFrame))
        self.updatecompbtn = Button(self, text="Update company", command=lambda: master.switch_frame(UpdateCompanyFrame))
        self.usrtocompbtn = Button(self, text="Add/remove users to/from company", command=lambda: master.switch_frame(UsersToCompanyFrame))

        self.psttransaction = Button(self, text="Add transaction", command=lambda: master.switch_frame(PostTransactionFrame))

        self.logoffbtn = Button(self, text="logoff", command=self._logoff_btn_clicked)
        #self.logoffbtn.grid(columnspan=2)



        self.label_welcome.grid(row=0, column=0, sticky=E)
        self.createusrbtn.grid(row=1, column=0, sticky=E)
        self.createcompbtn.grid(row=2, column=0, sticky=E)
        self.updatecompbtn.grid(row=3, column=0, sticky=E)
        self.usrtocompbtn.grid(row=4, column=0, sticky=E)
        self.psttransaction.grid(row=1, column=3, sticky=E)      #work on shifting these later
        self.logoffbtn.grid(row=2, column=3, sticky=E)




        self.pack()

    def _logoff_btn_clicked(self):
        sessionid = None #delete the session
        #print(sessionid)
        self.master.switch_frame(LoginFrame)

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
        name = self.entry_name.get()
        print(sessionid)

        API.createCompany(name,sessionid).subscribe(on_next=lambda response: {
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

class PostTransactionFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

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
    #lf = LoginFrame(app)
    #app.geometry('500x300')
    app.mainloop()
