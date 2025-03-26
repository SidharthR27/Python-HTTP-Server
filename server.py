import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 1234))
server_socket.listen(5)

(client_socket, client_address) = server_socket.accept()

data = client_socket.recv(1024)
print('Data from client received')

# send back same data
client_socket.sendall(data)
print('Data to client sent')

client_socket.close()
server_socket.close()