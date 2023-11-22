import socket
import threading

nicknames = {}

def broadcast(message):
    print(message)
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            if message == b'close':
                break

            nickname = nicknames[client]
            broadcast(f"{nickname}: {message}".encode('utf-8'))
        except:
            break

    client.close()
    del clients[clients.index(client)]
    broadcast(f"{nickname} has left the chat!".encode('utf-8'))

clients = []

host = '127.0.0.1'
port = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
print(f"Сервер слухає на {host}:{port}")

while True:
    client_socket, addr = server_socket.accept()
    print(f"З'єднано з {addr}")

    nickname = client_socket.recv(1024).decode('utf-8')
    nicknames[client_socket] = nickname
    clients.append(client_socket)

    print(f"{nickname} has joined the chat!")
    broadcast(f"{nickname} has joined the chat!".encode('utf-8'))

    client_thread = threading.Thread(target=handle, args=(client_socket,))
    client_thread.start()