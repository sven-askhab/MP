import threading
import time

def child_thread():
    i = 0
    while True:
        print(f"Дочерний поток: строка {i+1}")
        i += 1
        time.sleep(0.5)

thread = threading.Thread(target=child_thread)
thread.start()
time.sleep(2)

# В Python нет прямого аналога pthread_cancel, используем флаг
thread.running = False  # Для этого нужно модифицировать функцию потока
print("Родительский поток: запрос на завершение дочернего потока")