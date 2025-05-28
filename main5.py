import threading
import time
import sys

def cleanup():
    print("Дочерний поток: выполняется очистка перед завершением")

def child_thread():
    try:
        i = 0
        while True:
            print(f"Дочерний поток: строка {i+1}")
            i += 1
            time.sleep(0.5)
    finally:
        cleanup()

thread = threading.Thread(target=child_thread)
thread.start()
time.sleep(2)

# Эмуляция отмены через sys.exit()
print("Родительский поток: запрос на завершение дочернего потока")
sys.exit()  # Это завершит все потоки