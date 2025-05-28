import threading
import time


class SortedList:
    def __init__(self):
        self.head = None
        self.lock = threading.Lock()

    def insert(self, data):
        with self.lock:
            new_node = Node(data)
            if not self.head or data <= self.head.data:
                new_node.next = self.head
                self.head = new_node
            else:
                current = self.head
                while current.next and current.next.data < data:
                    current = current.next
                new_node.next = current.next
                current.next = new_node

    def display(self):
        with self.lock:
            current = self.head
            while current:
                print(current.data)
                current = current.next


def sleep_sort(s, sorted_list, factor=0.1):
    time.sleep(len(s) * factor)
    sorted_list.insert(s)


def main():
    import sys
    lines = [line.strip() for line in sys.stdin if line.strip()]
    sorted_list = SortedList()
    threads = []

    for line in lines:
        t = threading.Thread(target=sleep_sort, args=(line, sorted_list))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    sorted_list.display()


if __name__ == "__main__":
    main()