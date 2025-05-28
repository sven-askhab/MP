import threading
import time

def print_message(msg):
    for i in range(5):
        print(f"{msg} (строка {i+1})")
        time.sleep(0.5)

messages = [
    "Поток 1 сообщает",
    "Поток 2 говорит",
    "Поток 3 информирует",
    "Поток 4 передает"
]

threads = []
for msg in messages:
    t = threading.Thread(target=print_message, args=(msg,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()