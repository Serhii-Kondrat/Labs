import socket
import threading

def receive():
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            print(message)
        except:
            print("Від'єднано від сервера")
            break

def write():
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))
        if message == 'close':
            break

host = '127.0.0.1'
port = 12345

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

nickname = input("Введіть ваш нік: ")
client_socket.send(nickname.encode('utf-8'))

print(f"З'єднано з сервером {host}:{port}")

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write()

client_socket.close()