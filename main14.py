import threading


def child_thread(sem_parent, sem_child):
    for i in range(10):
        sem_child.acquire()  # Ждем разрешения на вывод
        print(f"Дочерний поток: строка {i + 1}")
        sem_parent.release()  # Разрешаем родительскому потоку выводить


def main():
    # Создаем два семафора:
    # sem_parent - контролирует вывод родительского потока (начальное значение 1)
    # sem_child - контролирует вывод дочернего потока (начальное значение 0)
    sem_parent = threading.Semaphore(1)
    sem_child = threading.Semaphore(0)

    thread = threading.Thread(target=child_thread, args=(sem_parent, sem_child))
    thread.start()

    for i in range(10):
        sem_parent.acquire()  # Ждем разрешения на вывод
        print(f"Родительский поток: строка {i + 1}")
        sem_child.release()  # Разрешаем дочернему потоку выводить

    thread.join()


if __name__ == "__main__":
    main()