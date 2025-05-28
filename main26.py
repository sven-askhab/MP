import threading
import time


class MessageQueueCV:
    def __init__(self):
        self.queue = []
        self.max_size = 10
        self.max_msg_size = 80
        self.dropped = False
        self.lock = threading.Lock()
        self.not_empty = threading.Condition(self.lock)
        self.not_full = threading.Condition(self.lock)

    def put(self, msg):
        with self.not_full:
            if self.dropped:
                return 0

            while len(self.queue) >= self.max_size and not self.dropped:
                self.not_full.wait()

            if self.dropped:
                return 0

            msg = msg[:self.max_msg_size]
            msg_length = len(msg)
            self.queue.append(msg)
            self.not_empty.notify()

            return msg_length

    def get(self, buf_size):
        with self.not_empty:
            if self.dropped and not self.queue:
                return ""

            while not self.queue and not self.dropped:
                self.not_empty.wait()

            if self.dropped and not self.queue:
                return ""

            msg = self.queue.pop(0)
            msg_length = min(len(msg), buf_size - 1)
            msg_to_return = msg[:msg_length]
            self.not_full.notify()

            return msg_to_return

    def drop(self):
        with self.lock:
            self.dropped = True
            self.not_empty.notify_all()
            self.not_full.notify_all()


def producer_cv(queue, id):
    for i in range(5):
        msg = f"Сообщение {i} от производителя {id}"
        length = queue.put(msg)
        print(f"Производитель {id} отправил: {msg[:20]}... ({length} chars)")
        time.sleep(0.5)
    print(f"Производитель {id} завершил работу")


def consumer_cv(queue, id):
    while True:
        msg = queue.get(100)
        if not msg:
            print(f"Потребитель {id} получил сигнал завершения")
            break
        print(f"Потребитель {id} получил: {msg[:20]}...")
        time.sleep(1)


def main_cv():
    queue = MessageQueueCV()

    producers = [
        threading.Thread(target=producer_cv, args=(queue, 1)),
        threading.Thread(target=producer_cv, args=(queue, 2))
    ]

    consumers = [
        threading.Thread(target=consumer_cv, args=(queue, 1)),
        threading.Thread(target=consumer_cv, args=(queue, 2))
    ]

    for p in producers:
        p.start()
    for c in consumers:
        c.start()

    time.sleep(3)
    print("\nИнициируем остановку...")
    queue.drop()

    for p in producers:
        p.join()
    for c in consumers:
        c.join()


if __name__ == "__main__":
    main_cv()