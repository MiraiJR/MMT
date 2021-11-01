import socket
import tkinter as tk 
from tkinter import messagebox
from tkinter import ttk 
from tkinter import *
import threading
import pyodbc
from tkinter import Entry, Tk
import tkinter.font
import tkinter.font as fnt
import json,urllib.request

import time

HOST = "127.0.0.1"
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



# server infor
serverName = "TRUONGVANHAO\SQLEXPRESS"
databaseAccount = "account_socket"
databaseCurency = "1"

FONT_Nueva = "Nueva Std Cond"


# lay du lieu tu json 
def getDataFromJson():
    data = urllib.request.urlopen("https://static.pipezero.com/covid/data.json").read()
    output = json.loads(data)   
    dataCovidVN = output['locations']
    listAll = []  
    for row in dataCovidVN:
        list = []
        province = row['name']
        death = row['death']
        treating = row['treating']
        cases = row['cases']
        recovered = row['recovered']
        casesToday = row['casesToday']
        list.append(province)
        list.append(death)
        list.append(treating)
        list.append(cases)
        list.append(recovered)
        list.append(casesToday)           
        listAll.append(list)
    return listAll
    



# tai khoan dang hoat dong
liveAcc = []

userAcc = []

userAddr = []



# kiem tra tai khoan dang hoat dong
def checkLiveAccount(username):
    for row in liveAcc:
        temp = str(row).find("-")
        userk = str(row[(temp+1):])
        if userk == username:
            return False
    return True
    


# Tao tai khoan moi
def createNewAccount(username, password):
    cursor = connectToDatabase()
    cursor.execute("insert into User_account(username,password) values(?,?);", (username, password))
    cursor.commit()
    

def removeActiveAccount(conn, addr):
    for row in liveAcc:
        temp = str(row).find("-")
        temp_check = str(row[:temp])
        if temp_check == str(addr):
            temp = str(row).find("-")
            userAddr.remove(temp_check)
            username = str(row[(temp+1):])
            userAcc.remove(username)
            liveAcc.remove(row)
            # conn.sendall("True".encode(FORMAT))
            
# Client dang nhap vao
def clientLogin(sck, addr):
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
            userAcc.append(username)
            userAddr.append(str(addr))
            account=str(userAddr[userAddr.__len__()-1])+"-"+str(userAcc[userAcc.__len__()-1])
            liveAcc.append(account)
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
                sck.sendall("False".encode(FORMAT))
                check = False
    if check == True:
        sck.sendall("True".encode(FORMAT))
        createNewAccount(username, password)
        print("Sign up successfully!") 

# client tim kiem du lieu
def clientSearchInfo(sck):
    dataCovid = getDataFromJson()
    
    inputsearch = sck.recv(1024).decode(FORMAT)
    
    print("Search: ", inputsearch)
    
    sck.sendall(inputsearch.encode(FORMAT))
    
    checkInp = False
    temp = []
    for row in dataCovid:
        if str(row[0]) == inputsearch:
            temp = row
            checkInp = True
            sck.sendall("True".encode(FORMAT))
            break
    
    
    
    if checkInp == True:
        startSend = sck.recv(1024).decode(FORMAT)
        if startSend == "start":
            for item in temp:
                kj = str(item)
                sck.sendall(kj.encode(FORMAT))
                sck.recv(1024)
            sck.sendall("end".encode(FORMAT))
    else:
        sck.sendall("False".encode(FORMAT))
            
    



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
            clientLogin(conn, addr)        
        elif option == SIGNUP:
            clientSignup(conn)
        elif option == LOGOUT:
            print("Client: ", addr, " disconnected")
            removeActiveAccount(conn, addr)
        elif option == SEARCH:
            clientSearchInfo(conn)
            
    
        
            
    
    
    
# khoi dong server
def runServer():
    try:
        print(HOST, PORT)
        print("Waiting for Client")
        while True:
            conn, addr = SERVER.accept()
            print("Client: ", addr, " connected")
            
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
        self.geometry("720x480")
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
        for F in (viewConnectedClients,dataPage, startPage, adminPage):
            frame = F(container, self)
            frame.grid(row = 0, column = 0, sticky="nsew")
            self.frames[F] = frame
        self.frames[startPage].tkraise()
    def showPage(self, FrameClass):
        self.frames[FrameClass].tkraise()
    
    
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
            self.showPage(adminPage)
            curFrame.label_notice["text"]=""
        else:
            curFrame.label_notice["text"] = "Username or password don't correct!"
    
    
        
       

        
        
        
        
        
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
        

        label_title = ttk.Label(self, background = "yellow",foreground="blue" ,text="\nLOGIN SERVER\n",font=(FONT_Nueva, 30, "bold"))
        label_title.configure(width=500,anchor="n")
        label_pass = ttk.Label(self, text="Password",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
        
        self.label_notice = ttk.Label(self,text="",background = "#ffbee3",foreground="red")
        
        
        label_user = ttk.Label(self, text="Username",foreground="blue",background = "#ffbee3",font=(FONT_Nueva, 14))
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
        self.configure(bg="#ffbee3")
        
        style = ttk.Style(self)
        
        
        
        btn_viewData = tk.Button(self,text="VIEW DATA COVID IN VIETNAM",font = fnt.Font(size = 10),cursor= "hand1", command = lambda: app_controller.showPage(dataPage)) 
        btn_viewData.configure(width=40)
        
        btn_viewClient = tk.Button(self,text="VIEW ACTIVE CLIENTS",font = fnt.Font(size = 10),cursor= "hand1", command = lambda: app_controller.showPage(viewConnectedClients)) 
        btn_viewClient.configure(width=40)

        btn_viewData.pack(pady=10)
        btn_viewClient.pack(pady=10)     
    
        
   
class viewConnectedClients(tk.Frame):
    def __init__(self, parent, app_controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg="#ffbee3")
        
        style = ttk.Style(self)
    
    
        self.label_title = ttk.Label(self, text="\n ACTIVE CLIENS \n",background = "#ffbee3", font=(FONT_Nueva, 30, "bold")).pack()
        
        btn_refresh = ttk.Button(self,text="REFRESH",cursor= "hand1",command =self.updateDataClient)
        btn_back = ttk.Button(self,text="BACK",cursor= "hand1",command = lambda: app_controller.showPage(adminPage))
        btn_refresh.configure(width=20)
        btn_back.configure(width=20)
        style.configure("mystyle.Treeview" ,background = "#44d2a8", highlightthickness=1, bd=1, font=('Times New Roman', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=(FONT_Nueva, 15,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        columns = ("Address", "Username")
        self.table = ttk.Treeview(self,style="mystyle.Treeview",selectmode='browse',columns=columns, show='headings')
        self.table.heading("Address", text="Address", anchor=tk.CENTER)
        self.table.heading("Username", text="Username", anchor=tk.CENTER)

        
        self.table.pack()
        btn_refresh.pack()
        btn_back.pack(pady=5)
    def updateDataClient(self):
        self.table.delete(*self.table.get_children())
        for row in liveAcc:
            temp = str(row).find("-")
            addressk = str(row[:temp])
            username = str(row[(temp+1):])
            self.table.insert('', tk.END, values=(addressk, username))
            
        

        
        
class dataPage(tk.Frame):
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
        
        self.label_title = ttk.Label(self, text="\n COVID IN VIETNAM \n",background = "#ffbee3", font=(FONT_Nueva, 30, "bold")).pack()
        
        
        btn_refresh = ttk.Button(self,text="REFRESH",cursor= "hand1",command =self.updateData)
        btn_back = ttk.Button(self,text="BACK",cursor= "hand1",command = lambda: app_controller.showPage(adminPage))
        
        style.configure("mystyle.Treeview" ,background = "#44d2a8", highlightthickness=1, bd=1, font=('Times New Roman', 12)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=(FONT_Nueva, 15,'bold')) # Modify the font of the headings
        style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        columns = ("Tỉnh/Thành phố", "Tử vong", "Chữa trị", "Ca mắc", "Phục hồi", "Ca mắc hôm nay")
        self.table = ttk.Treeview(self,style="mystyle.Treeview",selectmode='browse',columns=columns, show='headings')
        self.table.heading("Tỉnh/Thành phố", text="Tỉnh/Thành phố", anchor=tk.CENTER)
        self.table.heading("Tử vong", text="Tử vong", anchor=tk.CENTER)
        self.table.heading("Chữa trị", text="Chữa trị", anchor=tk.CENTER)
        self.table.heading("Ca mắc", text="Ca mắc", anchor=tk.CENTER)
        self.table.heading("Phục hồi", text="Phục hồi", anchor=tk.CENTER)
        self.table.heading("Ca mắc hôm nay", text="Ca mắc hôm nay", anchor=tk.CENTER)
        
        btn_refresh.configure(width=20)
        btn_back.configure(width=20)
        
        self.table.pack()
        
        btn_refresh.pack(pady=5)
        btn_back.pack(pady=5)
        
        
        
    def updateData(self):
        self.table.delete(*self.table.get_children())
        time.sleep(1)
        dataCorona = getDataFromJson()
        for row in dataCorona:
            self.table.insert('',tk.END, values=(row))
            
        
            
    
    
   
        
        
        
        
        
        
        
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen()

# Da luong ket noi 
sThread = threading.Thread(target=runServer)
sThread.daemon = False
sThread.start()

app = serverCurrencyExchange()
app.mainloop()
