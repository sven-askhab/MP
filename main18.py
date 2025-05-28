import threading
import time


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.lock = threading.Lock()


class LinkedList:
    def __init__(self):
        self.head = None
        self.head_lock = threading.Lock()

    def add(self, data):
        new_node = Node(data)
        with self.head_lock:
            new_node.next = self.head
            self.head = new_node

    def display(self):
        current = self.head
        while current:
            with current.lock:
                print(current.data)
                current = current.next

    def bubble_sort_step(self):
        if not self.head:
            return False

        changed = False
        prev = None
        current = self.head

        # Захватываем первые два узла
        if current:
            current.lock.acquire()
        if current and current.next:
            current.next.lock.acquire()

        while current and current.next:
            if current.data > current.next.data:
                # Захватываем prev если есть
                if prev:
                    prev.lock.acquire()

                # Меняем узлы местами
                if prev:
                    prev.next = current.next
                    prev.lock.release()
                else:
                    with self.head_lock:
                        self.head = current.next

                temp = current.next.next
                current.next.next = current
                current.next = temp

                # Обновляем prev и current
                prev = current.next
                changed = True

                # Захватываем следующий узел если есть
                if current.next and current.next.next:
                    current.next.next.lock.acquire()
            else:
                # Освобождаем предыдущий узел если был
                if prev:
                    prev.lock.release()
                prev = current
                current = current.next

                # Захватываем следующий узел если есть
                if current and current.next:
                    current.next.lock.acquire()

        # Освобождаем оставшиеся блокировки
        if prev:
            prev.lock.release()
        if current:
            current.lock.release()

        return changed


def sort_thread(linked_list):
    while True:
        time.sleep(1)
        while linked_list.bubble_sort_step():
            pass


def main():
    linked_list = LinkedList()

    # Добавление тестовых данных
    for word in ["banana", "apple", "cherry", "date"]:
        linked_list.add(word)

    sort_t = threading.Thread(target=sort_thread, args=(linked_list,))
    sort_t.daemon = True
    sort_t.start()

    while True:
        linked_list.display()
        time.sleep(2)


if __name__ == "__main__":
    main()