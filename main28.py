import sys
import socket
import select
import urllib.parse


def http_client(url):
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

    lines_printed = 0
    buffer = b''

    while True:
        readable, _, _ = select.select([s], [], [], 0.1)

        if s in readable:
            data = s.recv(4096)
            if not data:
                break
            buffer += data

            while b'\n' in buffer:
                line, buffer = buffer.split(b'\n', 1)
                print(line.decode().strip())
                lines_printed += 1

                if lines_printed % 25 == 0:
                    input("Press space to scroll down...")
        else:
            # Проверяем ввод пользователя без блокировки
            r, _, _ = select.select([sys.stdin], [], [], 0.1)
            if r:
                input()  # Ожидаем нажатия Enter

    s.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python http_client.py <url>")
        sys.exit(1)

    http_client(sys.argv[1])