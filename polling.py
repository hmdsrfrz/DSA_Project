import os
import time
import sys
import hashlib
import threading
from data_structures import HashTable
from file_lock import file_lock
from user_management import UserManagement
from driver_management import DriverManagement


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

user_mgmt = UserManagement()
driver_mgmt = DriverManagement()
hash_table = HashTable()

def calculate_file_hash(filename):
    """Calculate the hash of a file."""
    try:
        with open(filename, 'rb') as f:
            file_content = f.read()
            return hashlib.sha256(file_content).hexdigest()
    except FileNotFoundError:
        return None

def poll_file(filename, callback, poll_interval=1):
    """
    Polls a file for changes and reloads it using a callback when modified.
    Uses a lock to synchronize file access.
    """
    last_hash = calculate_file_hash(filename)

    while True:
        time.sleep(poll_interval)  # Wait for the next poll cycle
        with file_lock:  # Lock the file during hash calculation
            current_hash = calculate_file_hash(filename)

        if current_hash != last_hash:
            print(f"File {filename} has been updated. Reloading...")
            with file_lock:  # Lock the file during reload
                callback(filename)
            last_hash = current_hash

def reload_users(filename):
    """
    Reloads the user data from the specified file and updates the user management system.
    """
    try:
        user_mgmt.users.load_from_file(filename)
        print(f"User data reloaded from {filename}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"An error occurred while reloading users: {e}")

def reload_drivers(filename):
    """
    Reloads the driver data from the specified file and updates the driver management system.
    """
    try:
        driver_mgmt.drivers.load_from_file(filename)
        print(f"Driver data reloaded from {filename}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"An error occurred while reloading drivers: {e}")