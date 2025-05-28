import threading
import time


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def add(self, data):
        with self.lock:
            new_node = Node(data)
            new_node.next = self.head
            self.head = new_node

    def display(self):
        with self.lock:
            current = self.head
            while current:
                print(current.data)
                current = current.next

    def bubble_sort(self):
        with self.lock:
            if not self.head:
                return

            changed = True
            while changed:
                changed = False
                prev = None
                current = self.head

                while current and current.next:
                    if current.data > current.next.data:
                        if prev:
                            prev.next = current.next
                        else:
                            self.head = current.next

                        temp = current.next.next
                        current.next.next = current
                        current.next = temp

                        prev = current.next
                        changed = True
                    else:
                        prev = current
                        current = current.next


def input_thread(linked_list):
    while True:
        user_input = input("Введите строку (пустая для вывода): ")
        if not user_input:
            linked_list.display()
        else:
            for line in [user_input[i:i + 80] for i in range(0, len(user_input), 80)]:
                linked_list.add(line)


def sort_thread(linked_list):
    while True:
        time.sleep(5)
        linked_list.bubble_sort()


def main():
    linked_list = LinkedList()

    input_t = threading.Thread(target=input_thread, args=(linked_list,))
    sort_t = threading.Thread(target=sort_thread, args=(linked_list,))

    input_t.daemon = True
    sort_t.daemon = True

    input_t.start()
    sort_t.start()

    input_t.join()
    sort_t.join()


if __name__ == "__main__":
    main()