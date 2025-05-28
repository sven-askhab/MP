import time

class ReadWriteLinkedListWithDelay(ReadWriteLinkedList):
    def bubble_sort_step(self):
        with self.write_lock, self.rw_lock:
            # Логика сортировки из задания 18
            time.sleep(1)  # Добавляем задержку
            return changed

        prev = None
        current = self.head
        next_node = current.next

        current.lock.acquire()
        next_node.lock.acquire()
        if prev:
            prev.lock.acquire()

        changed = False
        try:
            if current.data > next_node.data:
                # Меняем узлы местами
                if prev:
                    prev.next = next_node
                else:
                    with self.head_lock:
                        self.head = next_node

                current.next = next_node.next
                next_node.next = current
                changed = True
        finally:
            if prev:
                prev.lock.release()
            next_node.lock.release()
            current.lock.release()

        time.sleep(1)  # Задержка между шагами
        return changed