import socket
import sys
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading
import time
import tkinter.font as fnt
import tkinter.font
from typing import Literal
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
READ = "read"


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
        self.iconbitmap('Images\covid.ico')
        self.geometry("1080x600")
        self.resizable(100, 100)
        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", rowheight=20, font=('Times New Roman', 10))
        style.configure("Treeview.Heading", font=(FONT_Nueva, 13,'bold'))
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'blue'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'red'),
                            ('active', 'blue')])
        
        container = tk.Frame()
        container.configure(bg="red")
        
        container.pack(side = "top", fill = "both", expand=True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in ( ipServer, startPage, homePage, signupPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[ipServer].tkraise()
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container==homePage:
            self.geometry("1080x600")
        else:
            self.geometry("1080x600")
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
            if inputsearch == "": #chuoi rong
                curFrame.label_notice["text"] = "Empty values!"
                return
            
            option = SEARCH 
            sck.sendall(option.encode(FORMAT)) # gui option search cho server
            
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
                curFrame.label_notice["text"] = "Value don't exist. Please inputing the correct value!"
                
        except:
            print("Error: Server is not responding")
            messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
            
    def dataPrint(self, sck):
        try:
            dataRecv = []
            sck.sendall("read".encode(FORMAT)) # gui option search cho server
            item = sck.recv(1024).decode(FORMAT)
            while item != "endrow":
                while item != "end":
                    sck.sendall(item.encode(FORMAT))
                    dataRecv.append(item)
                    item = sck.recv(1024).decode(FORMAT)
                sck.sendall(item.encode(FORMAT))
                item = sck.recv(1024).decode(FORMAT)
                dataSearch.append(dataRecv.copy())
                dataRecv.clear()
        
        except:
            print("error")
    def getIp(self, curFrame):
        HOST = curFrame.entry_ip.get()
        if HOST != "":
            try:
                server_addr = (HOST, PORT)
                CLIENT.connect(server_addr)
                self.showFrame(homePage)
                self.dataPrint(CLIENT)
            except:
                messagebox.showerror(title="ERROR", message="ERROR! CLIENT CAN'T CONNECT TO SERVER")
                print("ERROR! CLIENT CAN'T CONNECT TO SERVER")
        else:
            messagebox.showerror(title="ERROR", message="IP SERVER DON'T CORRECT")
        
class startPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")
        image = Image.open("Images/bg_login_client.png")
        image = image.resize((1080,600), Image.ANTIALIAS)
        
        self.img = ImageTk.PhotoImage(image)
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
        label_user = ttk.Label(self, text="Username : ",foreground="blue",background = "white",font=(FONT_Nueva, 14))
        self.entry_user = ttk.Entry(self,width=30)
        
        label_pass = ttk.Label(self, text="Password : ",foreground="blue",background = "white",font=(FONT_Nueva, 14))
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        
        self.label_notice = ttk.Label(self,foreground="red",background = "white",text="")
        
        button_log = ttk.Button(self,text="LOG IN",cursor= "hand1",  command = lambda: app_controller.loginApp(self, CLIENT)) 
        button_log.configure(width=20)
        button_sign = ttk.Button(self,text="SIGN UP",cursor= "hand1", command = lambda: app_controller.showPage(signupPage)) 
        button_sign.configure(width=20)
        
        label_user.place(x=70, y=280)
        self.entry_user.place(x=200, y=282)
        label_pass.place(x=72, y=330)
        self.entry_pass.place(x=200, y=332)
        self.label_notice.place(x=180, y=365)
        button_log.place(x=180, y=395)
        button_sign.place(x=180, y=430)

class signupPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")

        image = Image.open("Images/bg_signup_clients.png")
        image = image.resize((1080,600), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
    
        label_user = ttk.Label(self, text="Username :",foreground="blue",background = "white",font=(FONT_Nueva, 14))
        self.entry_user = ttk.Entry(self,width=30)
        
        label_pass = ttk.Label(self, text="Password :",foreground="blue",background = "white",font=(FONT_Nueva, 14))
        self.entry_pass = ttk.Entry(self,width=30,show="*")
        
        label_passAgain = ttk.Label(self, text="Password again :",foreground="blue",background = "white",font=(FONT_Nueva, 14))
        self.entry_passAgain = ttk.Entry(self,width=30,show="*")
        
        self.label_notice = ttk.Label(self,text="",foreground="red",background = "white",)
        
        button_log = ttk.Button(self,text="RETURN LOG IN", cursor= "hand1", command = lambda: app_controller.showPage(startPage)) 
        button_log.configure(width=20)
        button_sign = ttk.Button(self,text="SIGN UP", cursor= "hand1", command = lambda: app_controller.signupApp(self, CLIENT)) 
        button_sign.configure(width=20)
        
        label_user.place(x=86, y=250)
        self.entry_user.place(x=200, y=252)
        label_pass.place(x=88, y=300)
        self.entry_pass.place(x=200, y=302)
        label_passAgain.place(x=37, y=350)
        self.entry_passAgain.place(x=200, y=352)
        self.label_notice.place(x=180, y=385)
        button_log.place(x=180, y=405)
        button_sign.place(x=180, y=440)
        
class homePage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")

        image = Image.open("Images/bg_coviddata.png")
        image = image.resize((1080,600), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
         
        self.label_search = ttk.Label(self, text="Search : ", foreground="#3251A2", background = "white", font=(FONT_Nueva, 14))
        self.label_notice = ttk.Label(self, text="", foreground="red", background = "white")
        
        self.entry_search = ttk.Entry(self, width=40, font=("Times New Roman", 15))
        
        self.btn_search = tk.Button(self, text=" SEARCH ",font = fnt.Font(size = 13), cursor= "hand1",
                                    command = lambda: [app_controller.searchData(self, CLIENT), self.after(500, self.updateData)])
        self.btn_refresh = ttk.Button(self,text="REFRESH",cursor= "hand1",command =self.updateData)
        
        tree_frame = Frame(self) #Create Frame
        tree_frame.place(x=540,y=280, anchor=CENTER)
        tree_scroll = Scrollbar(tree_frame) #Create Scrollbar for table
        tree_scroll.pack(side=RIGHT, fill = Y)
        
        columns = ("Tỉnh/Thành phố", "Ca mắc", "Ca mắc hôm nay", "Tử vong")
        self.table = ttk.Treeview(tree_frame, style="mystyle.Treeview", selectmode='browse', columns=columns, show='headings', 
                                  yscrollcommand=tree_scroll.set)
        tree_scroll.config(command=self.table.yview)
        
        self.table.heading("Tỉnh/Thành phố", text="Tỉnh/Thành phố", anchor=tk.CENTER)
        self.table.heading("Ca mắc", text="Ca mắc", anchor=tk.CENTER)
        self.table.heading("Ca mắc hôm nay", text="Ca mắc hôm nay", anchor=tk.CENTER)
        self.table.heading("Tử vong", text="Tử vong", anchor=tk.CENTER)
        self.table.column("Ca mắc", anchor=CENTER)
        self.table.column("Ca mắc hôm nay", anchor=CENTER)
        self.table.column("Tử vong", anchor=CENTER)
        self.after(100, self.updateData())
        self.after(200, self.updateData())
        
        self.table.pack()
        self.label_search.place(x=280, y=417)
        self.entry_search.place(x=570, y=430, anchor=CENTER)
        self.label_notice.place(x=540, y=460, anchor=CENTER)
        self.btn_search.place(x=540, y=495, anchor=CENTER)
        self.btn_refresh.place(x=540, y=540, anchor=CENTER)
         
    def updateData(self):
        self.table.delete(*self.table.get_children())
        for row in dataSearch:
            self.table.insert('',tk.END, values=(row))
            
class ipServer(tk.Frame): #page nhap dia chi ip server
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="white")
        
        image = Image.open("Images/bg_input_IP.png")
        image = image.resize((1080,600), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(image)
        bg_label = ttk.Label(self, image=self.img)
        bg_label.place(x=0,y=0)
        
        self.entry_ip = ttk.Entry(self, width=40, font=("Time New Roman", 15), justify = CENTER)
        
        btn = ttk.Button(self, text="CONNECT",cursor= "hand1", command = lambda: app_controller.getIp(self))
        btn.configure(width=30)

        self.entry_ip.place(x=30, y=280)
        btn.place(x=152, y=330)
        
app = currencyExchangeRate_VietNam_App()
app.mainloop()