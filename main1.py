import threading
import time

def child_thread():
    for i in range(10):
        print(f"Дочерний поток: строка {i+1}")
        time.sleep(0.5)

thread = threading.Thread(target=child_thread)
thread.start()

for i in range(10):
    print(f"Родительский поток: строка {i+1}")
    time.sleep(0.5)

thread.join()