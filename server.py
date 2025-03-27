import socket

class MyServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 1234))
        self.server_socket.listen(5)
    
    def run_server(self):
        while True:
            (client_socket, client_address) = self.server_socket.accept()
            request_data = client_socket.recv(1024)
            print('Data from client received')
            method, path = self.find_request_method(request_data)
            if method == "GET":
                self.get_response(client_socket,client_address,request_data)
            elif method == "POST":
                pass
            else:
                return "HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed"

    
    def find_request_method(self,request_data):
        request_data = request_data.decode()
        headers, body = request_data.split("\r\n\r\n", 1) if "\r\n\r\n" in request_data else (request_data, "")
        lines = headers.split("\r\n")
        request_line = lines[0].split()
        
        if len(request_line) < 2:
            return "HTTP/1.1 400 Bad Request\r\n\r\nBad Request"

        method, path = request_line[:2]
        print(method,path)
        return (method,path)

    def get_response(self,client_socket,client_address,request_data):
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
                    <pre>{request_data.decode("utf-8")}</pre>
                </body>
            </html>
            \r\n\r\n
            """, "utf-8")
        )
        print('Data to client sent')
        client_socket.close()
        # server_socket.close()
    
    def post_response(self,client_socket,client_address,request_data):
        pass

my_server = MyServer()
my_server.run_server()
