import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('localhost', 1234))

message = "Testing..."
client_socket.send(message.encode())
print('Data to server send')

response = client_socket.recv(1024).decode()
print(f"Received from server: {response}")

client_socket.close()