
import os
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def poll_file(filename, hash_table, interval=5):
    last_modified = None
    while True:
        try:
            current_modified = os.path.getmtime(filename)
            if last_modified is None or current_modified > last_modified:
                print(f"{filename} has been updated. Reloading...")
                hash_table.load_from_file(filename)
                last_modified = current_modified
        except FileNotFoundError:
            print(f"{filename} not found. Skipping...")
        time.sleep(interval)
