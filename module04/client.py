import socket
import threading

# Server Configuration
HOST = '127.0.0.1'  # Server IP address (localhost for testing)
PORT = 12345        # Server Port

# Creating a socket object
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Receive messages from the server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            # Close the connection if there's an error
            print("An error occurred!")
            client.close()
            break

# Send messages to the server
def send():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('utf-8'))


if __name__ == '__main__':
    # Enter your nickname
    nickname = input("Choose your nickname: ")

    # Start the threads for receiving and sending messages
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()
