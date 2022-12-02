import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
 
# 引入chat.py
 
PORT = 5000
SERVER = "172.25.240.1"
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
 
# 創建一個新的 client socket
# 並連接到伺服器
client = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
client.connect(ADDRESS)
 
 
# GUI class for the chat
class GUI:
    # 建構式
    def __init__(self):
        

        # 把聊天介面設置成主介面
        self.Window = Tk()
        self.Window.withdraw() #隱藏
 
        # login 介面設置成子介面
        self.login = Toplevel()
        # 設置title
        self.login.title("Login")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        # 建立提示文字
        self.pls = Label(self.login,
                         text="建立帳號以加入聊天室",
                         justify=CENTER,
                         font="Helvetica 14 bold")
 
        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # 建立提示文字
        self.labelName = Label(self.login,
                               text="名稱: ",
                               font="Helvetica 12")
 
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
 
        # 輸入介面
        # 輸入資訊
        self.entryName = Entry(self.login,
                               font="Helvetica 14")
 
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        # 設置焦點在entryname
        self.entryName.focus()
 
        # 創建加入聊天室按鈕
        self.go = Button(self.login,
                         text="加入聊天室",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.go.place(relx=0.4,
                      rely=0.55)
        self.Window.mainloop()
 
    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
 
        # 建立子執行續
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # 主要的chatroom佈局
    def layout(self, name):
 
        self.name = name
        self.Window.deiconify() # 顯示chatroom
        self.Window.title(str(name+"的聊天室"))
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 

        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # 送出訊息
        
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        # 滾動欄
        scrollbar = Scrollbar(self.textCons)
 
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # 送出訊息
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # 接收訊息
    def receive(self):
        while True:
            try:
                message = client.recv(1024).decode(FORMAT)
 
                # if the messages from the server is NAME send the client's name
                if message == 'NAME':
                    client.send(self.name.encode(FORMAT))
                else:
                    # insert messages to text box
                    self.textCons.config(state=NORMAL)
                    self.textCons.insert(END,
                                         message+"\n\n")
 
                    self.textCons.config(state=DISABLED)
                    self.textCons.see(END)
            except:
                # 如果發生錯誤 跳出錯誤訊息
                print("An error occurred!")
                client.close()
                break
 
    # 送出訊息
    def sendMessage(self):
        self.textCons.config(state=DISABLED)
        while True:
            message = (f"{self.name}: {self.msg}")
            client.send(message.encode(FORMAT))
            break
 
 
# create a GUI class object
g = GUI()