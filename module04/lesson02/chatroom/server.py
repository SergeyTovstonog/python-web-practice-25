import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# Creating a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle individual client connection
def handle_client(client):
    while True:
        try:
            # Receive message from the client
            message = client.recv(1024)
            broadcast(message)
        except:
            # Remove and close the client connection if an error occurs
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# Receive new client connections
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        # Ask for the client's nickname
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        # Broadcast the new connection to all clients
        print(f"Nickname of the client is {nickname}")
        broadcast(f'{nickname} joined the chat! '.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        # Start handling the client's messages
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()



if __name__ == "__main__":
    print("Server is listening...")
    receive()