# import socket library
import socket
 
# import threading library
import threading
 
# 選擇伺服器的port
PORT = 5000
 
# 取得私人ip地址
SERVER = socket.gethostbyname(socket.gethostname())
 
# 儲存
ADDRESS = (SERVER, PORT)
 
# 設定編碼方式
FORMAT = "utf-8"
 
# 儲存所有連線的clients跟名稱
clients, names = [], []
 
# 建立新的socket給server
server = socket.socket(socket.AF_INET,
                       socket.SOCK_STREAM)
 
# 綁定address到server的socket
server.bind(ADDRESS)
 
# 開始連接(聊天)
 
def startChat():
 
    print("server is working on " + SERVER)
 
    # listening for connections
    server.listen()
 
    while True:
 
        # 輸出客戶端連接資訊
        conn, addr = server.accept()
        conn.send("NAME".encode(FORMAT))
 
        # 設定最大接收訊息的byte數
        name = conn.recv(1024).decode(FORMAT)
 
        # 儲存連接進來的用戶資訊
        names.append(name)
        clients.append(conn)
 
        print(f"Name is :{name}")
 
        # 廣播資訊
        broadcastMessage(f"{name} has joined the chat!".encode(FORMAT))
 
        conn.send('Connection successful!'.encode(FORMAT))
 
        # Start the handling thread
        thread = threading.Thread(target=handle,
                                  args=(conn, addr))
        thread.start()
 
        # no. of clients connected
        # to the server
        print(f"active connections {threading.active_count()-1}")
 

# 處理訊息
 
def handle(conn, addr):
 
    print(f"new connection {addr}")
    connected = True
 
    while connected:
          # 接收訊息
        message = conn.recv(1024)
 
        # 廣播訊息
        broadcastMessage(message)
 
    # 關閉連接
    conn.close()
 
# 廣播訊息給每個聊天室中的用戶

def broadcastMessage(message):
    for client in clients:
        client.send(message)
 
#開始server
startChat()