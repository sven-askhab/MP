import socket
import threading
import queue
import sys
from urllib.parse import urlparse
from collections import OrderedDict


class WorkerThread(threading.Thread):
    def __init__(self, task_queue, cache):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.cache = cache

    def run(self):
        while True:
            client_socket = self.task_queue.get()
            self.handle_client(client_socket)
            self.task_queue.task_done()

    def handle_client(self, client_socket):
        try:
            request = client_socket.recv(4096)
            if not request:
                return

            first_line = request.split(b'\n')[0]
            url = first_line.split()[1].decode()
            print(f"Request for {url}")

            cached = self.cache.get(url)
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

                self.cache.put(url, response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()


def run_thread_pool_proxy(proxy_port, num_workers=4):
    cache = ThreadedProxyCache()
    task_queue = queue.Queue()

    # Создаем пул рабочих потоков
    for _ in range(num_workers):
        worker = WorkerThread(task_queue, cache)
        worker.start()

    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', proxy_port))
    proxy_socket.listen(10)

    print(f"Thread pool proxy started on port {proxy_port} with {num_workers} workers")

    try:
        while True:
            client_socket, addr = proxy_socket.accept()
            print(f"New connection from {addr}")
            task_queue.put(client_socket)
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
    finally:
        proxy_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python thread_pool_proxy.py <proxy_port> <num_workers>")
        sys.exit(1)

    proxy_port = int(sys.argv[1])
    num_workers = int(sys.argv[2])
    run_thread_pool_proxy(proxy_port, num_workers)