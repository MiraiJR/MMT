import socket
import sys
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading
from types import NoneType
import time
import tkinter.font as fnt
import tkinter.font
from PIL import Image, ImageTk

HOST = ""
PORT = 65432
FORMAT = "utf8"
DISCONNECT = "x"

#option 
SIGNUP = "signup"
LOGIN = "login"
LOGOUT = "logout"
SEARCH = "search"


SUCCESS = "success"
FAIL = "fail"

FONT_Nueva = "Nueva Std Cond"

CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

dataSearch = []

#GUI DESIGN APP
class currencyExchangeRate_VietNam_App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Client App")
        self.iconbitmap('Images\money.ico')
        self.geometry("720x480")
        self.resizable(100, 100)
        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        container = tk.Frame()
        container.configure(bg="red")
        
        container.pack(side = "top", fill = "both", expand=True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in ( ipServer,startPage, homePage, signupPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[ipServer].tkraise()
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==homePage:
            self.geometry("720x480")
        else:
            self.geometry("720x480")
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
                return
                 
            # gửi option đến server
            option = LOGIN
            sck.sendall(option.encode(FORMAT))
            
            #gửi username và password đến server
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
                messagebox.showerror(title="ERROR", message="YOU CAN'T LOGIN WITH THIS ACCOUNT!")
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
    
    # client tim kiem du lieu 
    def searchData(self, curFrame, sck):
        try:
            dataRecv = []
            dataSearch.clear()
            inputsearch = curFrame.entry_search.get()
            if inputsearch == "":
                curFrame.label_notice["text"] = "Empty values!"
                return
            
            option = SEARCH
            sck.sendall(option.encode(FORMAT))
            
            sck.sendall(inputsearch.encode(FORMAT))
            print("Search: ", inputsearch)
            
            sck.recv(1024)
            print("Server responded") 
            
            accepted = sck.recv(1024).decode(FORMAT)
            print("Accepted: " + accepted)
            
            if accepted == "True":
                curFrame.label_notice["text"] = ""
                sck.sendall("start".encode(FORMAT))
                item = sck.recv(1024).decode(FORMAT)
                while(item != "end"):
                    sck.sendall(item.encode(FORMAT))
                    dataRecv.append(item)
                    item = sck.recv(1024).decode(FORMAT)
                    
                dataSearch.append(dataRecv)
                print(dataSearch)
            else:
                curFrame.label_notice["text"] = "Values don't exist. Please inputing the correct value!"
                
        except:
            print("Error: Server is not responding")
            messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
            
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
        else:
            messagebox.showerror(title="ERROR", message="IP SERVER DON'T CORRECT")
        
class startPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        self.img = ImageTk.PhotoImage(file="Images/abc.jpg")
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
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
        
        label_user = ttk.Label(self, text="Username ",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        self.entry_user = ttk.Entry(self,width=30)
        
        label_pass = ttk.Label(self, text="Password ",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        
        self.label_notice = ttk.Label(self,foreground="red",background = "#ffbee3",text="")
        
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

        self.img = ImageTk.PhotoImage(file="Images/abc.jpg")
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
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
        self.entry_user = ttk.Entry(self,width=30)
        
        label_pass = ttk.Label(self, text="Password",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        
        label_passAgain = ttk.Label(self, text="Password again",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        self.entry_passAgain = ttk.Entry(self,width=30,show="*")
        
        self.label_notice = ttk.Label(self,text="",foreground="red",background = "#ffbee3",)
        
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
        
class homePage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        self.img = ImageTk.PhotoImage(file="Images/abc.jpg")
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
        style = ttk.Style(self)
        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
        
        self.label_title = ttk.Label(self, background = "#ffbee3",text="HOMEPAGE",font=(FONT_Nueva, 30, "bold"))
        self.label_notice = ttk.Label(self,text="",foreground="red",background = "#ffbee3",)
        
        self.entry_search = ttk.Entry(self, width=40, font=("Times New Roman", 20))
        
        self.btn_search = tk.Button(self, text="SEARCH",font = fnt.Font(size = 20),cursor= "hand1",command = lambda: app_controller.searchData(self, CLIENT))
        self.btn_refresh = ttk.Button(self,text="REFRESH",cursor= "hand1",command =self.updateData)
        
        style.configure("mystyle.Treeview" ,background = "#44d2a8", highlightthickness=1, bd=1, font=('Times New Roman', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=(FONT_Nueva, 15,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        columns = ("Tỉnh/Thành phố", "Ca mắc", "Chữa trị", "Phục hồi", "Tử vong", "Ca mắc hôm nay")
        self.table = ttk.Treeview(self,style="mystyle.Treeview",selectmode='browse',columns=columns, show='headings')
        self.table.heading("Tỉnh/Thành phố", text="Tỉnh/Thành phố", anchor=tk.CENTER)
        self.table.heading("Ca mắc", text="Ca mắc", anchor=tk.CENTER)
        self.table.heading("Chữa trị", text="Chữa trị", anchor=tk.CENTER)
        self.table.heading("Phục hồi", text="Phục hồi", anchor=tk.CENTER)
        self.table.heading("Tử vong", text="Tử vong", anchor=tk.CENTER)
        self.table.heading("Ca mắc hôm nay", text="Ca mắc hôm nay", anchor=tk.CENTER)
        
        self.label_title.pack(pady=10)
        self.entry_search.pack(pady=10)
        self.label_notice.pack(pady=2)
        self.btn_search.pack(pady=5)
        self.btn_refresh.pack(pady=5)
        self.table.pack()
    def updateData(self):
        self.table.delete(*self.table.get_children())
        time.sleep(1)
        for row in dataSearch:
            self.table.insert('',tk.END, values=(row))
            
class ipServer(tk.Frame): #page nhap dia chi ip server
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")

        self.img = ImageTk.PhotoImage(file="Images/abc.jpg")
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
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
        
        self.entry_ip = ttk.Entry(self, width=40, font=("Time New Roman", 20))
        
        btn = ttk.Button(self, text="CONNECT",cursor= "hand1", command = lambda: app_controller.getIp(self))
        btn.configure(width=30)
        
        label_title.pack(pady=5)
        self.entry_ip.pack(pady=5)
        btn.pack(pady=5)
        
app = currencyExchangeRate_VietNam_App()
app.mainloop()