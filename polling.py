import os
import time
import sys
import hashlib
from data_structures import HashTable
from user_management import UserManagement
from driver_management import DriverManagement
from save_load import load_data_from_file
from data_structures import HashTable
from map_data import IslamabadMap

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
islamabad_map = IslamabadMap()
user_mgmt = UserManagement(islamabad_map)
driver_mgmt = DriverManagement()
hash_table = HashTable()

def calculate_file_hash(filename):
    """Calculate the hash of a file."""
    try:
        with open(filename, 'rb') as f:
            file_content = f.read()
            file_hash = hashlib.sha256(file_content).hexdigest()
            return file_hash
    except FileNotFoundError:
        print(f"Debug: File {filename} not found.")
        return None

def poll_file(filename, callback, poll_interval=1):
    """
    Polls a file for changes and reloads it using a callback when modified.
    """
    last_hash = calculate_file_hash(filename)

    while True:
        time.sleep(poll_interval)  # Wait for the next poll cycle
        current_hash = calculate_file_hash(filename)

        if current_hash != last_hash:
            print(f"File {filename} has been updated. Reloading...")
            callback(filename)
            last_hash = current_hash

def reload_users(filename):
    global user_mgmt
    try:
        new_users = load_data_from_file(filename, HashTable)
        if isinstance(new_users, HashTable):
            user_mgmt.users = new_users
            print(f"User data reloaded from {filename}.")
        else:
            print(f"Warning: Loaded data is not a HashTable. Resetting to empty.")
            user_mgmt.users = HashTable()
    
    except Exception as e:
        print(f"An error occurred while reloading users: {e}")

def reload_drivers(filename):
    global driver_mgmt
    try:
        new_drivers = load_data_from_file(filename, HashTable)
        if isinstance(new_drivers, HashTable):
            driver_mgmt.drivers = new_drivers
            print(f"Driver data reloaded successfully from {filename}.")
        else:
            print(f"Warning: Loaded data is not a HashTable. Resetting to empty.")
            driver_mgmt.drivers = HashTable()
    
    except Exception as e:
        print(f"An error occurred while reloading drivers: {e}")


