import threading
import sys


def calculate_partial_sum(start, end, result_list, index):
    partial = 0.0
    for i in range(start, end):
        term = 1.0 / (2 * i + 1)
        if i % 2 == 0:
            partial += term
        else:
            partial -= term
    result_list[index] = partial


def main():
    if len(sys.argv) != 3:
        print("Usage: python pi.py <num_threads> <num_iterations>")
        return

    num_threads = int(sys.argv[1])
    num_iterations = int(sys.argv[2])

    chunk_size = num_iterations // num_threads
    results = [0.0] * num_threads
    threads = []

    for i in range(num_threads):
        start = i * chunk_size
        end = (i + 1) * chunk_size if i != num_threads - 1 else num_iterations
        t = threading.Thread(target=calculate_partial_sum, args=(start, end, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    pi = 4.0 * sum(results)
    print(f"Calculated π = {pi:.15f}")


if __name__ == "__main__":
    main()