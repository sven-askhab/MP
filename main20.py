import threading


class ReadWriteLinkedList(LinkedList):
    def __init__(self):
        super().__init__()
        self.rw_lock = threading.RLock()
        self.readers = 0
        self.read_lock = threading.Lock()
        self.write_lock = threading.Lock()

    def add(self, data):
        with self.write_lock:
            new_node = Node(data)
            with self.head_lock:
                new_node.next = self.head
                self.head = new_node

    def display(self):
        with self.read_lock:
            self.readers += 1
            if self.readers == 1:
                self.rw_lock.acquire()

        current = self.head
        while current:
            with current.lock:
                print(current.data)
                current = current.next

        with self.read_lock:
            self.readers -= 1
            if self.readers == 0:
                self.rw_lock.release()

    def bubble_sort_step(self):
        with self.write_lock, self.rw_lock:
            # Остальная логика сортировки как в задании 18
            pass