import socket
import sys
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading
from types import NoneType
import time


HOST = "127.0.0.1"
PORT = 65432
FORMAT = "utf-8"
DISCONNECT = "x"

#option 
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"

SUCCESS = "success"
FAIL = "fail"




    



    

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
        for F in (startPage, homePage, signupPage, adminPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[startPage].tkraise()
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
    
    
        
class startPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        
        
          
        label_title = tk.Label(self, text="LOGIN", fg='#20639b',bg="bisque2",font=("Times New Roman", 16, "bold"))
        
        label_pass = tk.Label(self, text="Password ",fg='#20639b',bg="bisque2",font=("Times New Roman", 12))
        
        self.label_notice = tk.Label(self,text="",fg='red',bg="bisque2")
        
        label_user = tk.Label(self, text="Username ",fg='#20639b',bg="bisque2",font=("Times New Roman", 12))
        self.entry_user = tk.Entry(self,width=30,bg='light yellow')
        self.entry_pass = tk.Entry(self,width=30,show="*",bg='light yellow')
        
        button_log = tk.Button(self,text="LOG IN", bg="#20639b",fg='floral white', command = lambda: app_controller.loginApp(self, CLIENT)) 
        button_log.configure(width=20)
        button_sign = tk.Button(self,text="SIGN UP",bg="#20639b",fg='floral white', command = lambda: app_controller.showPage(signupPage)) 
        button_sign.configure(width=20)
        button_refresh = tk.Button(self,text="REFRESH",bg="#20639b",fg='floral white', command = lambda: app_controller.serverDisconnect(CLIENT)) 
        button_refresh.configure(width=20)
        
        
        label_title.pack(pady=5)
        label_user.pack()
        self.entry_user.pack()
        label_pass.pack()
        self.entry_pass.pack()
        self.label_notice.pack()

        button_log.pack(pady=5)
        button_sign.pack(pady=5)
        button_refresh.pack()
        
        
class signupPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        label_title = tk.Label(self, text="SIGNUP", fg='#20639b',bg="bisque2", font=("Times New Roman", 16, "bold"))
        label_user = tk.Label(self, text="Username",fg='#20639b',bg="bisque2",font=("Times New Roman", 12))
        label_pass = tk.Label(self, text="Password",fg='#20639b',bg="bisque2",font=("Times New Roman", 12))
        label_passAgain = tk.Label(self, text="Password again",fg='#20639b',bg="bisque2",font=("Times New Roman", 12))
        
        self.label_notice = tk.Label(self,text="",bg="bisque2")
        self.entry_user = tk.Entry(self,width=30,bg='light yellow')
        self.entry_pass = tk.Entry(self,width=30,show="*",bg='light yellow')
        self.entry_passAgain = tk.Entry(self,width=30,show="*",bg='light yellow')
        
        button_log = tk.Button(self,text="RETURN LOG IN", bg="#20639b",fg='floral white', command = lambda: app_controller.showPage(startPage)) 
        button_log.configure(width=20)
        button_sign = tk.Button(self,text="SIGN UP",bg="#20639b",fg='floral white',  command = lambda: app_controller.signupApp(self, CLIENT)) 
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
        self.configure(bg="bisque2")
        label_title = tk.Label(self, text="HOMEPAGE", fg='#20639b',bg="bisque2")
        label_title.pack()
        # tra cuu thong tin









try: 
    app = currencyExchangeRate_VietNam_App()
    CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_addr = (HOST, PORT)
    CLIENT.connect(server_addr)
    app.mainloop()
except:
    messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
    print("ERROR! CLIENT CAN'T CONNECT TO SERVER")
    CLIENT.close()
finally:
    CLIENT.close()
