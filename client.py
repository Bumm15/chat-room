import socket, time

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!disconnect"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)

def start():
    answer = input("Chceš se připojit (ano/ne)? ")
    if answer.lower() != "ano":
        return
    connection = connect()
    name = input(str("Jméno: "))
    if name != "":
        send(connection, ("$" + name))

    while True:
        msg = input("Message (q for quit): ")

        if msg == "q":
            break
        send(connection, msg)

    send(connection, DISCONNECT_MESSAGE)
    time.sleep(1)
    print("Odpojeno")

start()