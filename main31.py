import socket
import select
import sys
import threading
from urllib.parse import urlparse
from collections import OrderedDict


class ProxyCache:
    def __init__(self, max_size=100):
        self.cache = OrderedDict()
        self.max_size = max_size
        self.lock = threading.Lock()

    def get(self, url):
        with self.lock:
            if url in self.cache:
                self.cache.move_to_end(url)
                return self.cache[url]
        return None

    def put(self, url, data):
        with self.lock:
            self.cache[url] = data
            self.cache.move_to_end(url)
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)


def run_caching_proxy(proxy_port):
    cache = ProxyCache()
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', proxy_port))
    proxy_socket.listen(10)

    sockets = [proxy_socket]
    connections = {}

    print(f"Caching proxy started on port {proxy_port}")

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [])

            for sock in readable:
                if sock == proxy_socket:
                    client_socket, client_addr = proxy_socket.accept()
                    print(f"New connection from {client_addr}")

                    sockets.append(client_socket)
                    connections[client_socket] = {'buffer': b'', 'url': None}
                else:
                    try:
                        data = sock.recv(4096)
                        if not data:
                            raise ConnectionError("Connection closed")

                        conn_info = connections[sock]
                        conn_info['buffer'] += data

                        if b'\r\n\r\n' in conn_info['buffer'] and not conn_info['url']:
                            headers = conn_info['buffer'].split(b'\r\n\r\n')[0]
                            header_lines = headers.split(b'\r\n')
                            for line in header_lines:
                                if line.startswith(b'GET '):
                                    url = line.split()[1].decode()
                                    conn_info['url'] = url
                                    print(f"Request for {url}")

                                    cached = cache.get(url)
                                    if cached:
                                        print("Serving from cache")
                                        sock.sendall(cached)
                                        sock.close()
                                        sockets.remove(sock)
                                        del connections[sock]
                                        break
                    except Exception as e:
                        print(f"Connection error: {e}")
                        sock.close()
                        sockets.remove(sock)
                        if sock in connections:
                            del connections[sock]
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
    finally:
        for s in sockets:
            s.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python caching_proxy.py <proxy_port>")
        sys.exit(1)

    proxy_port = int(sys.argv[1])
    run_caching_proxy(proxy_port)