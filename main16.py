import multiprocessing as mp
import time


def child_process(sem_parent, sem_child):
    for i in range(10):
        sem_child.acquire()
        print(f"Дочерний процесс: строка {i + 1}")
        sem_parent.release()


def main():
    sem_parent = mp.Semaphore(1)
    sem_child = mp.Semaphore(0)

    p = mp.Process(target=child_process, args=(sem_parent, sem_child))
    p.start()

    for i in range(10):
        sem_parent.acquire()
        print(f"Родительский процесс: строка {i + 1}")
        sem_child.release()

    p.join()


if __name__ == "__main__":
    main()