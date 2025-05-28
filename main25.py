import threading
import time


class MessageQueue:
    def __init__(self):
        self.queue = []
        self.max_size = 10
        self.max_msg_size = 80
        self.dropped = False

        self.mutex = threading.Semaphore(1)
        self.items = threading.Semaphore(0)
        self.spaces = threading.Semaphore(self.max_size)

    def put(self, msg):
        if self.dropped:
            return 0

        msg = msg[:self.max_msg_size]
        msg_length = len(msg)

        self.spaces.acquire()
        self.mutex.acquire()

        if self.dropped:
            self.mutex.release()
            self.spaces.release()
            return 0

        self.queue.append(msg)
        self.mutex.release()
        self.items.release()

        return msg_length

    def get(self, buf_size):
        if self.dropped:
            return 0

        self.items.acquire()
        self.mutex.acquire()

        if self.dropped:
            self.mutex.release()
            self.items.release()
            return 0

        msg = self.queue.pop(0)
        msg_length = min(len(msg), buf_size - 1)
        msg_to_return = msg[:msg_length]

        self.mutex.release()
        self.spaces.release()

        return msg_to_return

    def drop(self):
        self.mutex.acquire()
        self.dropped = True
        self.mutex.release()

        # Разблокируем все ожидающие потоки
        for _ in range(self.max_size):
            self.spaces.release()
        for _ in range(self.max_size):
            self.items.release()


def producer(queue, id):
    for i in range(5):
        msg = f"Сообщение {i} от производителя {id}"
        length = queue.put(msg)
        print(f"Производитель {id} отправил: {msg[:20]}... ({length} chars)")
        time.sleep(0.5)
    print(f"Производитель {id} завершил работу")


def consumer(queue, id):
    while True:
        msg = queue.get(100)
        if not msg:
            print(f"Потребитель {id} получил сигнал завершения")
            break
        print(f"Потребитель {id} получил: {msg[:20]}...")
        time.sleep(1)


def main():
    queue = MessageQueue()

    producers = [
        threading.Thread(target=producer, args=(queue, 1)),
        threading.Thread(target=producer, args=(queue, 2))
    ]

    consumers = [
        threading.Thread(target=consumer, args=(queue, 1)),
        threading.Thread(target=consumer, args=(queue, 2))
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
    main()