import threading
import socket, time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

connected_clients = []

clients = set()
clients_lock = threading.Lock()

def handle_client(conn, addr):
    adress = addr
    print(f"[NEW CONNECTION] {adress} Connected")

    try:
        connected = True
        first_connection = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT)
            if not msg:
                break
            
            if msg.startswith("$") and first_connection:
                first_connection = False
                name = msg.upper()
                name_len = len(name)
                print("name: ", name[1:name_len])
                addr = name[1:name_len]

            if msg == DISCONNECT_MESSAGE:
                print(f"[SERVER]: Client {addr} has disconnected")
                connected = False
            else:
                if msg.startswith("$"):
                    pass
                else:
                    print(f"[{addr}]: {msg}")
                    with clients_lock:
                        for c in clients:
                            c.sendall(f"[{addr}]: {msg}".encode(FORMAT))

    finally:
        with clients_lock:
            clients.remove(conn)

        conn.close()

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def start():
    print("[SERVER]: Server is starting")
    time.sleep(.3)
    print("[SERVER]: Server has started")
    server.listen()
    while True:
        conn, addr = server.accept()
        with clients_lock:
            clients.add(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        connected_clients.append(addr)
        print(addr)
        print(connected_clients)
        send(connected_clients[0], "ahojky")

start()

