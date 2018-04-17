from Blockchain.Blockchain import Blockchain
from FineChainAPI import API
from FineChainAPI.Session import Session

from pprint import pprint
import json

from tkinter import *
import tkinter.messagebox as tm

class MainApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self._frame = None
        self.switch_frame(LoginFrame)
        self.geometry('500x300')

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

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

        self.checkbox = Checkbutton(self, text="Keep me logged in")
        self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.mainbtn = Button(self, text="Main Screen", command=lambda: master.switch_frame(MainFrame))
        self.mainbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        response = API.login(username, password).subscribe(on_next= lambda response: {
            pprint(response)

        })
        #display welcome in GUI if authenticated later

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        #Replace with logoffbtn function which sends to server to log off
        self.logoffbtn = Button(self, text="logoff", command=lambda: master.switch_frame(LoginFrame))
        self.logoffbtn.grid(columnspan=2)

    def _logoff_btn_clicked(self):
        return



if __name__ == '__main__':
    app = MainApp()
    app.title("FineChain")
    #lf = LoginFrame(app)
    #app.geometry('500x300')
    app.mainloop()
