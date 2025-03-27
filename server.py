import socket

class MyServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 1234))
        self.server_socket.listen(5)
    
    def run_server(self):
        while True:
            (client_socket, client_address) = self.server_socket.accept()
            data = client_socket.recv(1024)
            print('Data from client received')
            self.get_response(client_socket,client_address,data)

    def get_response(self,client_socket,client_address,data):
        # send back data
        client_socket.sendall(
            bytes(f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r\nSet-Cookie: ServerName=sidsPythonServer\r
            \r\n
            <!doctype html>
            <html>
                <head/>
                <body>
                    <h1>Welcome to the server!</h1>
                    <h2>Server address: 127.0.0.1:1234</h2>
                    <h3>You're connected through address: {client_address[0]}:{client_address[1]}</h3>
                    <body>
                        <pre>{data.decode("utf-8")}<pre>
                    </body>
                </body>
            </html>
            \r\n\r\n
            """, "utf-8")
        )
        print('Data to client sent')
        client_socket.close()
        # server_socket.close()

my_server = MyServer()
my_server.run_server()
