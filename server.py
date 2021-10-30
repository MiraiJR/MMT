
import socket
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading

import pyodbc
from tkinter import Entry, Tk

import requests

from bs4 import BeautifulSoup
import tkinter.font


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


# server infor
serverName = "TRUONGVANHAO\SQLEXPRESS"
databaseAccount = "account_socket"
databaseCurency = ""

FONT_Nueva = "Nueva Std Cond"


# lay du lieu tu html
URLWEB = "https://portal.vietcombank.com.vn/Usercontrols/TVPortal.TyGia/pXML.aspx"
def getDataFromHtml(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    data = soup.findAll("exrate")
    listAll=[]


    for row in data:
        list = []
        currencycode = row.get('currencycode')
        currencyname = row.get('currencyname')
        transfer = row.get('transfer')
        buy = row.get('buy')
        sell = row.get('sell')
        list.append(currencyname.strip())
        list.append(currencycode)
        list.append(buy)
        list.append(transfer)
        list.append(sell)
        listAll.append(list)

    return listAll;
    



# tai khoan dang hoat dong
liveAcc = []

# kiem tra tai khoan dang hoat dong
def checkLiveAccount(username):
    for row in liveAcc:
        if str(row) == username:
            return False
    return True


# Tao tai khoan moi
def createNewAccount(username, password):
    cursor = connectToDatabase()
    cursor.execute("insert into User_account(username,password) values(?,?);", (username, password))
    cursor.commit()
    


        
        
# Client dang nhap vao
def clientLogin(sck):
    print("Log in------------------------")
    username = sck.recv(1024).decode(FORMAT)
    print("Username: "+ username)
    sck.sendall(username.encode(FORMAT))
    
    password = sck.recv(1024).decode(FORMAT)
    print("Password: " + password)
    sck.sendall(password.encode(FORMAT))
    
    # 1. dang nhap thanh cong
    # 2. dang nhap that bai
    # 3. dand nhap vao admin
    # 4. tai khoan dang hoat dong nen khong the dang nhap
    
    if username == "admin" and password == "123456":
        sck.sendall("3".encode(FORMAT))
        return
    
    if checkLiveAccount(username) == False:
        sck.sendall("4".encode(FORMAT))
        return
    
    try:
        
        cursor = connectToDatabase()
        cursor.execute("select password from User_account where username = ?", username)
        check_password = cursor.fetchone()
        data_password = check_password[0].strip()
        if (data_password == password):
            print("Login successfully!")
            liveAcc.append(username)
            sck.sendall("1".encode(FORMAT))
        else:
            print("Invalid password!")
            sck.sendall("2".encode(FORMAT))
    except:
        print("Username is not correct!")
        sck.sendall("2".encode(FORMAT))
        
# client dang ky tai khoan moi
def clientSignup(sck):
    print("Sign up:-------------")
    username = sck.recv(1023).decode(FORMAT)
    print("Username: ", username)
    sck.sendall(username.encode(FORMAT))
    
    password = sck.recv(1024).decode(FORMAT)
    print("Password: ", password)
    sck.sendall(password.encode(FORMAT))
    
    # False. ton tai username
    cursor = connectToDatabase()
    cursor.execute("select username from User_account")
    
    check = True
    if(username == "admin"):
        sck.sendall("False".encode(FORMAT))
        check = False
    else:
        # kiem tra username co ton tai hay khong
        for row in cursor:
            if( str(row[0]).strip() == str(username)):
                print("sdasd")
                sck.sendall("False".encode(FORMAT))
                check = False
    if check == True:
        sck.sendall("True".encode(FORMAT))
        createNewAccount(username, password)
        print("Sign up successfully!")
        
    
    
    
    
    
    
            
            
            
    
    
    

# ket noi database tai khoan
def connectToDatabase():
    adminAcc = "admin" #tai khoan admin
    adminPass = "123456" 
    conx = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};\
                            SERVER="+serverName+";\
                            DATABASE="+databaseAccount+"; UID="+adminAcc+"; PWD="+adminPass+"")
    cursor = conx.cursor()
    return cursor

# xu ly client da dang nhap vao
def handleClient(conn, addr):
    
    while True:
        
        option = conn.recv(1024).decode(FORMAT)


        if option == LOGIN:
            clientLogin(conn)
        
        elif option == SIGNUP:
            clientSignup(conn)
        elif option == LOGOUT:
            print("Client disconnected!")
    
        
            
    
    
    
# khoi dong server
def runServer():
    try:
        print(HOST, PORT)
        print("Waiting for Client")
        while True:
            conn, addr = SERVER.accept()
            print("Client: ", addr, " connected")
            print("Conn: ", conn.getsockname())
            
            thr = threading.Thread(target=handleClient, args=(conn, addr))
            thr.daemon = True
            thr.start()
            
        
        
    except :
        
        print("SERVER is closed")
        SERVER.close()

        
    
    


# GUI DESIGN APP
class serverCurrencyExchange(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title("Server App")
        self.iconbitmap('Images\money.ico')
        self.geometry("500x300")
        self.resizable(100, 100)
        self.protocol("WM_DELETE_WINDOW", self.closeApp)
        
        container = tk.Frame()
        container.configure(bg="red")
        
        container = tk.Frame()
        container.configure(bg="red")
        container.pack(side = "top", fill = "both", expand=True)        
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (startPage, adminPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[startPage].tkraise()
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    def showFrame(self, container):
        frame = self.frames[container]
        if container == adminPage:
            self.geometry("450x500")
        else:
            self.geometry("500x200")
        frame.tkraise()
    # ask when quit
    def closeApp(self):
        if messagebox.askokcancel("Quit", "You really want to quit this usefull app ?"):
            SERVER.close()
            self.destroy()
            
            
    def loginServer(self, curFrame):
        
        username = curFrame.entry_user.get()
        password = curFrame.entry_pass.get()
        
        if password == "":
            curFrame.label_notice["text"] = "Please typing password!"
            
        if username == "admin" and password == "123456":
            self.showFrame(adminPage)
            curFrame.label_notice["text"]=""
        else:
            curFrame.label_notice["text"] = "Username or password don't correct!"
class startPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        style = ttk.Style(self)

        
        # thiet ke entry
        style.map('TEntry',   foreground=[
                    ('disabled', 'gray'),
                    ('focus !disabled', 'red'),
                    ('hover !disabled', 'blue')])
        # thiet ke button
        style.map('TButton', foreground=[('pressed', 'blue'),
                            ('active', 'red')])
        

        label_title = ttk.Label(self, background = "yellow",foreground="blue" ,text="\nLOGIN SERVER\n",font=(FONT_Nueva, 30, "bold"))
        label_title.configure(width=500,anchor="n")
        label_pass = ttk.Label(self, text="Password",foreground="blue",background = "bisque2",font=(FONT_Nueva, 14))
        
        self.label_notice = ttk.Label(self,text="",background = "bisque2",foreground="red")
        
        
        label_user = ttk.Label(self, text="Username",foreground="blue",background = "bisque2",font=(FONT_Nueva, 14))
        self.entry_user = ttk.Entry(self,width=40)
        self.entry_pass = ttk.Entry(self,width=40 ,show="*")
        
        
        button_log = ttk.Button(self,text="LOG IN",cursor= "hand1",command = lambda: app_controller.loginServer(self)) 
        button_log.configure(width=20)

        
        
        label_title.pack(pady=5)
        label_user.pack()
        self.entry_user.pack()
        label_pass.pack()
        self.entry_pass.pack()
        self.label_notice.pack()

        button_log.pack(pady=5)
        
        
        
class adminPage(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="bisque2")
        
        
        
        
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

# Da luong ket noi 
sThread = threading.Thread(target=runServer)
sThread.daemon = False
sThread.start()

app = serverCurrencyExchange()
app.mainloop()
