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
            file_hash = hashlib.sha256(file_content).hexdigest()
            #print(f"Debug: Calculated hash for {filename}: {file_hash}")  # Debugging statement
            return file_hash
    except FileNotFoundError:
        print(f"Debug: File {filename} not found.")
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
        user_mgmt.users.load_data_from_file(filename)
        print(f"User data reloaded from {filename}")
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
    except Exception as e:
        print(f"An error occurred while reloading users: {e}")

def reload_drivers(filename):
    """
    Reloads the driver data from the specified file and updates the driver management system.
    """
    print(f"Attempting to reload driver data from {filename}...")  # Debugging statement
    try:
        # Debugging: Check if the file exists before trying to load it
        if not os.path.exists(filename):
            print(f"Debug: File {filename} does not exist.")
            raise FileNotFoundError(f"{filename} not found.")

        # Attempt to load the driver data
        print("Debug: Calling load_from_file method...")
        driver_mgmt.drivers.load_data_from_file(filename)
        
        print(f"Driver data reloaded successfully from {filename}.")  # Debugging statement
    except FileNotFoundError:
        print(f"Error: {filename} not found.")  # Error message
    except Exception as e:
        print(f"An error occurred while reloading drivers: {e}")  # General error message