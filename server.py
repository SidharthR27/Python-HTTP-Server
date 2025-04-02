import socket
import sqlite3

class MyServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', 1234))
        self.server_socket.listen(5)

        self.init_db()

    def init_db(self):
        """Creates a database and a table if they don't exist"""
        conn = sqlite3.connect("server_data.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
    
    def run_server(self):
        try:
            while True:
                (client_socket, client_address) = self.server_socket.accept()
                request_data = client_socket.recv(1024)
                print('Data from client received')
                method, path, body = self.find_request_method(request_data)
                if method == "GET":
                    self.get_response(client_socket,client_address,request_data)
                elif method == "POST":
                    self.post_response(client_socket,client_address,body)
                else:
                    client_socket.sendall(b"HTTP/1.1 405 Method Not Allowed\r\n\r\nMethod Not Allowed")
                    client_socket.close()
        except KeyboardInterrupt:
            self.server_socket.close()
            print("Server socket closed.")

    def find_request_method(self,request_data):
        request_data = request_data.decode()
        headers, body = request_data.split("\r\n\r\n", 1) if "\r\n\r\n" in request_data else (request_data, "")
        lines = headers.split("\r\n")
        request_line = lines[0].split()
        
        if len(request_line) < 2:
            return "HTTP/1.1 400 Bad Request\r\n\r\nBad Request"

        method, path = request_line[:2]
        print(method,path)
        return (method,path,body)

    def get_response(self,client_socket,client_address,request_data):
        conn = sqlite3.connect("server_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        conn.close()

        messages_list = [f"<li>{row[1]}</li>" for row in rows]
        messages_html = "".join(messages_list)

        response = f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r\nSet-Cookie: ServerName=sidsPythonServer\r\n\r\n
        <!doctype html>
        <html>
            <body>
                <h1>Stored Messages</h1>
                <ul>{messages_html}</ul>
            </body>
        </html>
        """
        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()
    
    def post_response(self,client_socket,client_address,body):
        """Extract data from POST request and insert it into SQLite"""
        message = body.strip()
        
        conn = sqlite3.connect("server_data.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (message) VALUES (?)", (message,))
        conn.commit()
        conn.close()

        response = f"""HTTP/1.1 200 OK\r\nContent-type: text/html\r\nSet-Cookie: ServerName=sidsPythonServer\r\n\r\n
        <!doctype html>
        <html>
            <body>
                <h1>POST Request Received</h1>
                <p>Message stored in database: {message}</p>
            </body>
        </html>
        """
        client_socket.sendall(response.encode("utf-8"))
        client_socket.close()

my_server = MyServer()
my_server.run_server()
