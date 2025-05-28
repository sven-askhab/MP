import socket
import select
import sys


def run_proxy(local_port, remote_host, remote_port):
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    proxy_socket.bind(('0.0.0.0', local_port))
    proxy_socket.listen(10)

    sockets = [proxy_socket]
    connections = {}

    print(f"Proxy started on port {local_port}, forwarding to {remote_host}:{remote_port}")

    try:
        while True:
            readable, _, _ = select.select(sockets, [], [])

            for sock in readable:
                if sock == proxy_socket:
                    client_socket, client_addr = proxy_socket.accept()
                    print(f"New connection from {client_addr}")

                    try:
                        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        remote_socket.connect((remote_host, remote_port))

                        connections[client_socket] = remote_socket
                        connections[remote_socket] = client_socket
                        sockets.extend([client_socket, remote_socket])
                    except Exception as e:
                        print(f"Failed to connect to remote: {e}")
                        client_socket.close()
                else:
                    try:
                        data = sock.recv(4096)
                        if not data:
                            raise ConnectionError("Connection closed")

                        peer = connections[sock]
                        peer.sendall(data)
                    except Exception as e:
                        print(f"Connection error: {e}")
                        peer = connections.get(sock)
                        if peer:
                            sockets.remove(peer)
                            sockets.remove(sock)
                            peer.close()
                            sock.close()
                            del connections[peer]
                            del connections[sock]
    except KeyboardInterrupt:
        print("\nShutting down proxy...")
    finally:
        for s in sockets:
            s.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python proxy.py <local_port> <remote_host> <remote_port>")
        sys.exit(1)

    local_port = int(sys.argv[1])
    remote_host = sys.argv[2]
    remote_port = int(sys.argv[3])

    run_proxy(local_port, remote_host, remote_port)