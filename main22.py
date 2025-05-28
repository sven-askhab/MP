import threading
import time
import random

PHILOSOPHERS = 5
FOOD = 50
DELAY = 0.03

forks = [threading.Lock() for _ in range(PHILOSOPHERS)]
table_lock = threading.Lock()
cond = threading.Condition(table_lock)


def philosopher(id):
    left = id
    right = (id + 1) % PHILOSOPHERS

    while True:
        with table_lock:
            # Пытаемся взять обе вилки
            got_left = forks[left].acquire(False)
            if got_left:
                got_right = forks[right].acquire(False)
                if got_right:
                    # Успешно взяли обе вилки
                    pass
                else:
                    # Не смогли взять правую - отпускаем левую
                    forks[left].release()
                    cond.wait()
                    continue
            else:
                # Не смогли взять левую - ждем
                cond.wait()
                continue

        # Едим
        print(f"Философ {id} ест")
        time.sleep(DELAY * random.random())

        # Освобождаем вилки
        with table_lock:
            forks[left].release()
            forks[right].release()
            cond.notify_all()

        # Думаем
        print(f"Философ {id} размышляет")
        time.sleep(DELAY * random.random())


def main():
    philosophers = []
    for i in range(PHILOSOPHERS):
        p = threading.Thread(target=philosopher, args=(i,))
        philosophers.append(p)
        p.start()

    for p in philosophers:
        p.join()


if __name__ == "__main__":
    main()