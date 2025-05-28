import threading
import sys
import signal
import time

stop_flag = False
results_lock = threading.Lock()
results = []


def calculate_pi_part(start, chunk_size):
    partial = 0.0
    for i in range(start, start + chunk_size):
        if stop_flag:
            break
        term = 1.0 / (2 * i + 1)
        if i % 2 == 0:
            partial += term
        else:
            partial -= term
    with results_lock:
        results.append(partial)


def sigint_handler(signum, frame):
    global stop_flag
    stop_flag = True


def main():
    signal.signal(signal.SIGINT, sigint_handler)

    num_threads = 4
    chunk_size = 1000000

    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=calculate_pi_part, args=(i * chunk_size, chunk_size))
        threads.append(t)
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass

    for t in threads:
        t.join()

    pi = 4.0 * sum(results)
    print(f"\nApproximate π = {pi:.15f}")


if __name__ == "__main__":
    main()