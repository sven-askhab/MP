import threading
import time
import random

PHILOSOPHERS = 5
FOOD = 50
DELAY = 0.03

forks = [threading.Lock() for _ in range(PHILOSOPHERS)]
food_lock = threading.Lock()


def get_forks(left, right):
    while True:
        left_acquired = forks[left].acquire(False)
        if left_acquired:
            right_acquired = forks[right].acquire(False)
            if right_acquired:
                return
            else:
                forks[left].release()
        time.sleep(random.uniform(0.01, 0.1))


def philosopher(id):
    left_fork = id
    right_fork = (id + 1) % PHILOSOPHERS

    # Чтобы избежать deadlock, философ с четным ID берет сначала правую вилку
    if id % 2 == 0:
        first_fork, second_fork = right_fork, left_fork
    else:
        first_fork, second_fork = left_fork, right_fork

    while True:
        with food_lock:
            if FOOD <= 0:
                break
            FOOD -= 1
            current_food = FOOD

        print(f"Philosopher {id} is thinking about dish {current_food}")
        time.sleep(DELAY * random.random())

        print(f"Philosopher {id} is hungry for dish {current_food}")

        get_forks(first_fork, second_fork)
        print(f"Philosopher {id} is eating dish {current_food}")
        time.sleep(DELAY * random.random())

        forks[first_fork].release()
        forks[second_fork].release()

    print(f"Philosopher {id} is done eating")


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