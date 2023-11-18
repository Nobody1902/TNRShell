import socket
import os
import time
import threading
from rich.console import Console
CONSOLE = Console()

# Message info
HEADER = int(os.environ.get("MESSAGE_HEADER", 64))
FORMAT = os.environ.get("MESSAGE_FORMAT", "utf-8")
DISCONNECT_MSG = os.environ.get("DISCONNECT_MSG", "!DISCONNECT")

# Server info
SERVER = socket.gethostbyname(socket.gethostname())
PORT = os.environ.get("SERVER_PORT", 5050)
ADDR = (SERVER, int(PORT))

# Creating the server socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

# Send to client
def send(msg:str, conn:socket.socket):
    message = msg.encode(FORMAT)

    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    # Pad the send lenght
    send_lenght += b" " * (HEADER-len(send_lenght))

    conn.send(send_lenght)
    conn.send(message)

# Handle the connection
def handle_client(conn: socket.socket, addr, stopEvent:threading.Event):
    #CONSOLE.print(f"[yellow][SERVER] [green]{addr[0]}:{addr[1]} connected to server.")

    while True:
        if stopEvent.is_set():
            break
        try:
            msg_lenght = conn.recv(HEADER).decode(FORMAT)
            if not msg_lenght:
                continue
            msg_lenght = int(msg_lenght)

            msg = conn.recv(msg_lenght).decode(FORMAT)

            if msg == DISCONNECT_MSG:
                #CONSOLE.print(f"[red][SERVER] {addr[0]}:{addr[1]} disconnected.")
                connections.remove((addr,conn))
                break

            CONSOLE.print("[white]", end="")
            CONSOLE.print(f"{msg}", end="", markup=False)
            CONSOLE.print(f"[blue]{addr[0]}:{addr[1]}[white]>", end="")
        except:
            break
    
    conn.close()

connections: list[tuple[tuple[str,int],socket.socket]] = []

# Recieve connections
def start(stopEvent: threading.Event):
    server.listen()
    while True:
        try:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr, stopEvent,))
            connections.append((addr, conn))
            thread.name = str(addr)
            thread.start()
        except:
            break


def print_input(msg:str):
    try:
        return CONSOLE.input(msg, markup=False)
    except:
        return False


def client_selected(index:int):
    ip = connections[index][0][0]
    port = connections[index][0][1]
    conn = connections[index][1]
    CONSOLE.print(f"\n[blue]{ip}:{port}[white]>", end="")
    while True:
        command = print_input("")
        if command == "":
            send("", conn)
            continue
        if command == False:
            CONSOLE.print(end="")
            break

        if command == "!exit":
            break
        
        if command == "!close" or command == "!stop":
            conn.close()
            connections.remove(connections[index])
            CONSOLE.print(f"[red]Closed connection with {ip}:{port}")
            break

        send(command, conn)
        time.sleep(1)

stopEvent = threading.Event()

CONSOLE.print("[green][SERVER] Server is starting...")
CONSOLE.print(f"[green][SERVER] Server is running on {SERVER}:{PORT}")
listeningThread = threading.Thread(target=start, args=(stopEvent,))
listeningThread.start()


while True:
    command = print_input("> ")
    if command == "list":
        # print all ongoing connections
        for i, client in enumerate(connections):
            CONSOLE.print(f"{i+1}. [yellow]{client[0][0]}:{client[0][1]}")
    
    if command == "exit" or command == False:
        stopEvent.set()
        server.close()
        for c in connections:
            c[1].close()
        break

    if command == "cls" or command == "clear":
        CONSOLE.clear()
        CONSOLE.print(f"[green][SERVER] Server is running on {SERVER}:{PORT}")
        continue

    if command.split(" ")[0] == "select" or command.split(" ")[0] == "sel":
        try:
            # parse for hostname
            ip = ""
            port = 0
            if command.split(" ")[1][0] == ".":
                ip = connections[int(command.split(" ")[1].removeprefix("."))-1][0][0]
                port = connections[int(command.split(" ")[1].removeprefix("."))-1][0][1]
            else:
                ip = command.split(" ")[1].split(":")[0]
                port = int(command.split(" ")[1].split(":")[1])
            
            # check if client is connected
            connection_index = -1
            for i,c in enumerate(connections):
                if c[0] == (ip,port):
                    connection_index = i
                    break
            else:
                CONSOLE.print("[red]Client doesn't exist.")
                continue
            
            # the client messaging
            client_selected(connection_index)
            continue

        except:
            CONSOLE.print("[red]Invalid syntax.")