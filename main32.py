import socket
import threading
import sys
from urllib.parse import urlparse
from collections import OrderedDict


class ThreadedProxyCache:
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


def handle_client(client_socket, cache):
    try:
        request = client_socket.recv(4096)
        if not request:
            return

        first_line = request.split(b'\n')[0]
        url = first_line.split()[1].decode()
        print(f"Request for {url}")

        cached = cache.get(url)
        if cached:
            print("Serving from cache")
            client_socket.sendall(cached)
            return

        parsed = urlparse(url)
        host = parsed.netloc
        path = parsed.path or '/'

        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = 80

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.connect((host, port))
            server_socket.send(request)

            response = b''
            while True:
                data = server_socket.recv(4096)
                if not data:
                    break
                response += data
                client_socket.send(data)

            cache.put(url, response)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()


def run_threaded_proxy(proxy_port):
    cache = ThreadedProxyCache()
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', proxy_port))
    proxy_socket.listen(10)

    print(f"Threaded caching proxy started on port {proxy_port}")

    try:
        while True:
            client_socket, addr = proxy_socket.accept()
            print(f"New connection from {addr}")

            thread = threading.Thread(
                target=handle_client,
                args=(client_socket, cache),
                daemon=True
            )
            thread.start()
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
    finally:
        proxy_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python threaded_proxy.py <proxy_port>")
        sys.exit(1)

    proxy_port = int(sys.argv[1])
    run_threaded_proxy(proxy_port)