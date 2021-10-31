import socket
import sys
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading
from types import NoneType
import time

import tkinter.font
HOST = ""
PORT = 65432
FORMAT = "utf-8"
DISCONNECT = "x"

#option 
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"

SUCCESS = "success"
FAIL = "fail"

FONT_Nueva = "Nueva Std Cond"

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#GUI DESIGN APP
class currencyExchangeRate_VietNam_App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Client App")
        self.iconbitmap('Images\money.ico')
        self.geometry("500x300")
        self.resizable(100, 100)
        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        container = tk.Frame()
        container.configure(bg="red")
        
        container.pack(side = "top", fill = "both", expand=True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in ( ipServer,startPage, homePage, signupPage, adminPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[ipServer].tkraise()
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==homePage:
            self.geometry("700x500")
        elif container == adminPage:
            self.geometry("450x500")
        else:
            self.geometry("500x200")
        frame.tkraise()
        

    
        
    # ask when quit
    def closeApp(self):
        if messagebox.askokcancel("Quit", "You really want to quit this usefull app ?"):
            self.destroy()
            try: 
                option = LOGOUT;
                CLIENT.sendall(option.encode(FORMAT))
            except:
                pass
    # login
    def loginApp(self, curFrame, sck):
        try: 
            username = curFrame.entry_user.get()
            password = curFrame.entry_pass.get()
            if username == "" or password == "":
                curFrame.label_notice["text"] = "Fields cannot be empty"
                 
            
            # Notice to server for starting log in
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            
            #send username and password to server 
            sck.sendall(username.encode(FORMAT))
            print("Input: ", username)
            
            sck.recv(1024)
            print("Server responded")                  
            
            sck.sendall(password.encode(FORMAT))
            print("Input: ", password)
            
            sck.recv(1024)
            print("Server responded")   
                 
            accepted = sck.recv(1024).decode(FORMAT)
            print("Accepted: " + accepted)
            
            if accepted == "4":
                curFrame.label_notice["text"] = "Fail to log in!"
                if messagebox.askokcancel("Notice", "The account is active in another client!"):
                    pass
            elif accepted == "3":
                if messagebox.askokcancel("Notice", "Welcome, Admin."):
                    self.showFrame(adminPage) 
            elif accepted == "2":
                curFrame.label_notice["text"] = "Username or password don't correct! Please try again!"
            elif  accepted == "1":           
                self.showFrame(homePage)
                
            
                
            
            
        except:
            messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
            
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")
    
    # sign up
    def signupApp(self, curFrame, sck):
        try: 
            username = curFrame.entry_user.get()
            password = curFrame.entry_pass.get()
            passwordAga = curFrame.entry_passAgain.get()
            
            if(password != passwordAga):
                curFrame.label_notice["text"] = "Password again don't correct!"
                return
            
            
            option = SIGNUP 
            sck.sendall(option.encode(FORMAT))                                   
            
            sck.sendall(username.encode(FORMAT))
            print("Input: ", username)
            
            sck.recv(1024)
            print("Server responded") 
            
            sck.sendall(password.encode(FORMAT))
            print("Input: ", password)
            
            sck.recv(1024)
            print("Server responded")
            
            accepted = sck.recv(1024).decode(FORMAT)
            print("Accepted: " + accepted)
            
            if accepted == "True":
                self.showFrame(startPage)
                curFrame.label_notice["text"] = ""
            else:
                curFrame.label_notice["text"] = "Username already exists. Please using other username!"
               
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")
            
    # logout account 
    def logoutApp(self,curFrame, sck):
        try:
            option = LOGOUT
            sck.sendall(option.encode(FORMAT))
            accepted = sck.recv(1024).decode(FORMAT)
            if accepted == "True":
                self.showFrame(startPage)
        except:
            curFrame.label_notice["text"] = "Error: Server is not responding"
            print("Error: Server is not responding")
    
    def getIp(self, curFrame):
        HOST = curFrame.entry_ip.get()
        if HOST != "":
            try:
                server_addr = (HOST, PORT)
                CLIENT.connect(server_addr)
                self.showFrame(startPage)
            except:
                messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
                print("ERROR! CLIENT CAN'T CONNECT TO SERVER")
                CLIENT.close()
            
        else:
            messagebox.showerror(title="ERROR", message="IP SERVER DON'T CORRECT")
            
            
    
        
class startPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        
        style = ttk.Style(self)

        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
          
        label_title = ttk.Label(self, text="LOGIN", foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 30, "bold"))
        
        label_pass = ttk.Label(self, text="Password ",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        
        self.label_notice = ttk.Label(self,foreground="red",background = "#ffbee3",text="")
        
        label_user = ttk.Label(self, text="Username ",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        self.entry_user = ttk.Entry(self,width=30)
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        
        button_log = ttk.Button(self,text="LOG IN",cursor= "hand1",  command = lambda: app_controller.loginApp(self, CLIENT)) 
        button_log.configure(width=20)
        button_sign = ttk.Button(self,text="SIGN UP",cursor= "hand1", command = lambda: app_controller.showPage(signupPage)) 
        button_sign.configure(width=20)

        
        
        label_title.pack(pady=5)
        label_user.pack()
        self.entry_user.pack()
        label_pass.pack()
        self.entry_pass.pack()
        self.label_notice.pack()

        button_log.pack(pady=5)
        button_sign.pack(pady=5)

        
        
class signupPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        style = ttk.Style(self)

        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
        
        
        label_title = ttk.Label(self, text="SIGNUP", foreground="blue",background = "#ffbee3", font=(FONT_Nueva, 30, "bold"))
        label_user = ttk.Label(self, text="Username",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        label_pass = ttk.Label(self, text="Password",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        label_passAgain = ttk.Label(self, text="Password again",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        
        self.label_notice = ttk.Label(self,text="",foreground="red",background = "#ffbee3",)
        self.entry_user = ttk.Entry(self,width=30)
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        self.entry_passAgain = ttk.Entry(self,width=30,show="*")
        
        button_log = ttk.Button(self,text="RETURN LOG IN", cursor= "hand1", command = lambda: app_controller.showPage(startPage)) 
        button_log.configure(width=20)
        button_sign = ttk.Button(self,text="SIGN UP", cursor= "hand1", command = lambda: app_controller.signupApp(self, CLIENT)) 
        button_sign.configure(width=20)
        
        
        label_title.pack(pady=5)
        label_user.pack()
        self.entry_user.pack()
        label_pass.pack()
        self.entry_pass.pack()
        label_passAgain.pack()
        self.entry_passAgain.pack()
        self.label_notice.pack()

        button_log.pack(pady=5)
        button_sign.pack()
class adminPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        
        
class homePage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        style = ttk.Style(self)

        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
        
        self.label_title = ttk.Label(self, background = "#ffbee3",text="HOMEPAGE",font=(FONT_Nueva, 30, "bold")).grid(row=0, column=0, sticky=E)
        
        self.entry_search = ttk.Entry(self, width=40, font=(FONT_Nueva, 14)).grid(row=1, column=0, sticky=E)
        
        self.btn_search = ttk.Button(self, text="SEARCH",cursor= "hand1").grid(row=1,column=0, sticky=E)
        
        
        
        
        
        
        
        
        
        
        # tra cuu thong tin
class ipServer(tk.Frame): #page nhap dia chi ip server
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        style = ttk.Style(self)

        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
        
        label_title = ttk.Label(self, text="INPUT IP SERVER", foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 30, "bold"))
        
        self.entry_ip = ttk.Entry(self, width=40, font=(FONT_Nueva, 14))
        
        btn = ttk.Button(self, text="CONNECT",cursor= "hand1", command = lambda: app_controller.getIp(self))
        btn.configure(width=30)
        
        label_title.pack(pady=5)
        self.entry_ip.pack(pady=5)
        btn.pack(pady=5)
        
        
app = currencyExchangeRate_VietNam_App()
app.mainloop()