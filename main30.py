import threading
import socket
import sys
import queue


def reader_thread(sock, output_queue):
    while True:
        data = sock.recv(4096)
        if not data:
            output_queue.put(None)
            break
        output_queue.put(data)


def http_client_threaded(url):
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc
    path = parsed.path or '/'

    if ':' in host:
        host, port = host.split(':')
        port = int(port)
    else:
        port = 80

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    s.send(request.encode())

    output_queue = queue.Queue()
    reader = threading.Thread(target=reader_thread, args=(s, output_queue))
    reader.daemon = True
    reader.start()

    lines_printed = 0

    while True:
        data = output_queue.get()
        if data is None:
            break

        for line in data.split(b'\n'):
            print(line.decode().strip())
            lines_printed += 1

            if lines_printed % 25 == 0:
                input("Press space to scroll down...")

    s.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python threaded_http_client.py <url>")
        sys.exit(1)

    http_client_threaded(sys.argv[1])