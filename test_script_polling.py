import threading
import time
import json

from polling import poll_file
from data_structures import HashTable

hash_table = HashTable()

# Start polling in a separate thread
poller_thread = threading.Thread(target=poll_file, args=('test_data.json', hash_table))
poller_thread.daemon = True
poller_thread.start()

# Simulate file updates
time.sleep(5)  # Let the poller run
with open('test_data.json', 'w') as f:
    json.dump({
        "driver_1": {
            "id": "driver_1",
            "name": "Jane Doe",
            "ride_history": ["ride_3"]
        }
    }, f)

time.sleep(5)  # Allow poller to reload the updated file
print(f"HashTable contents: {hash_table.table}")
