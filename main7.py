import os
import shutil
import sys
import threading
import time


def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print(f"Error copying {src}: {e}")


def process_directory(src_root, dst_root, path=''):
    src_path = os.path.join(src_root, path)
    dst_path = os.path.join(dst_root, path)

    os.makedirs(dst_path, exist_ok=True)

    threads = []
    for entry in os.listdir(src_path):
        full_src = os.path.join(src_path, entry)
        full_dst = os.path.join(dst_path, entry)

        if os.path.isdir(full_src):
            t = threading.Thread(target=process_directory, args=(src_root, dst_root, os.path.join(path, entry)))
            threads.append(t)
            t.start()
        elif os.path.isfile(full_src):
            t = threading.Thread(target=copy_file, args=(full_src, full_dst))
            threads.append(t)
            t.start()

    for t in threads:
        t.join()


def main():
    if len(sys.argv) != 3:
        print("Usage: python mt_cp.py <source> <destination>")
        return

    src = sys.argv[1]
    dst = sys.argv[2]

    if not os.path.isdir(src):
        print(f"Source directory {src} does not exist")
        return

    process_directory(src, dst)


if __name__ == "__main__":
    main()