import socket
import os
import mimetypes
from datetime import datetime

HOST = '127.0.0.1'
PORT = 8080
WWW_DIR = './www'

def log_request(method, path, response_code):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] \"{method} {path}\" {response_code}")

def handle_request(client_socket):
    request_data = client_socket.recv(1024).decode()
    if not request_data:
        client_socket.close()
        return

    request_line = request_data.splitlines()[0]
    parts = request_line.split()
    if len(parts) < 2:
        client_socket.close()
        return

    method, path = parts[0], parts[1]
    if method != 'GET':
        client_socket.close()
        return

    if path == '/':
        path = '/index.html'

    file_path = os.path.normpath(os.path.join(WWW_DIR, path.lstrip('/')))
    
    if os.path.commonprefix((os.path.realpath(file_path), os.path.realpath(WWW_DIR))) != os.path.realpath(WWW_DIR):
        response_code = 403
        response = f"HTTP/1.1 {response_code} Forbidden\r\n\r\nForbidden"
        client_socket.sendall(response.encode())
        client_socket.close()
        return

    if os.path.exists(file_path) and os.path.isfile(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        mime_type, _ = mimetypes.guess_type(file_path)
        response_code = 200
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {mime_type or 'application/octet-stream'}\r\n\r\n"
        client_socket.sendall(response.encode() + content)
    else:
        response_code = 404
        custom_404_path = os.path.join(WWW_DIR, '404.html')
        if os.path.exists(custom_404_path) and os.path.isfile(custom_404_path):
            with open(custom_404_path, 'rb') as f:
                content = f.read()
            mime_type = 'text/html'
            header = f"HTTP/1.1 404 Not Found\r\nContent-Type: {mime_type}\r\n\r\n"
            client_socket.sendall(header.encode() + content)
        else:
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<h1>404 Not Found</h1>"
            client_socket.sendall(response.encode())

    log_request(method, path, response_code)
    client_socket.close()

def run_server():
    if not os.path.isdir(WWW_DIR):
        print(f"Errore: Directory '{WWW_DIR}' non trovata")
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            server_socket.bind((HOST, PORT))
        except OSError as e:
            print(f"Errore bind {HOST}:{PORT} - {e}")
            return
        server_socket.listen(5)
        print(f"Server in esecuzione su http://{HOST}:{PORT}/")

        while True:
            client_socket, _ = server_socket.accept()
            handle_request(client_socket)

if __name__ == '__main__':
    run_server()
