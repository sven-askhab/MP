import threading
import time
from collections import deque


class ProductionLine:
    def __init__(self):
        self.sem_a = threading.Semaphore(0)
        self.sem_b = threading.Semaphore(0)
        self.sem_c = threading.Semaphore(0)
        self.sem_module = threading.Semaphore(0)
        self.sem_widget = threading.Semaphore(0)
        self.widget_count = 0
        self.lock = threading.Lock()

    def produce_part_a(self):
        while True:
            time.sleep(1)  # Производство детали A занимает 1 секунду
            print("Произведена деталь A")
            self.sem_a.release()

    def produce_part_b(self):
        while True:
            time.sleep(2)  # Производство детали B занимает 2 секунды
            print("Произведена деталь B")
            self.sem_b.release()

    def produce_part_c(self):
        while True:
            time.sleep(3)  # Производство детали C занимает 3 секунды
            print("Произведена деталь C")
            self.sem_c.release()

    def assemble_module(self):
        while True:
            self.sem_a.acquire()
            self.sem_b.acquire()
            time.sleep(0.5)  # Сборка модуля из A и B
            print("Собран модуль (A+B)")
            self.sem_module.release()

    def assemble_widget(self):
        while True:
            self.sem_module.acquire()
            self.sem_c.acquire()
            time.sleep(1)  # Сборка винтика из модуля и C
            with self.lock:
                self.widget_count += 1
            print(f"Собран винтик (модуль+C). Всего: {self.widget_count}")
            self.sem_widget.release()

    def run(self):
        threads = [
            threading.Thread(target=self.produce_part_a),
            threading.Thread(target=self.produce_part_b),
            threading.Thread(target=self.produce_part_c),
            threading.Thread(target=self.assemble_module),
            threading.Thread(target=self.assemble_widget)
        ]

        for t in threads:
            t.daemon = True
            t.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nПроизводство остановлено")


if __name__ == "__main__":
    factory = ProductionLine()
    factory.run()