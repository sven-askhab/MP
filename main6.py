import threading
import time
import sys


def sleep_print(s, factor=0.1):
    time.sleep(len(s) * factor)
    print(s)


def main():
    lines = [line.strip() for line in sys.stdin if line.strip()]
    threads = []

    for line in lines:
        t = threading.Thread(target=sleep_print, args=(line,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    main()