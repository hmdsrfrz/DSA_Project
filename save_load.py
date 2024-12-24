#save_load.py

import json
from file_lock import file_lock

def save_data_to_file(data, filename):
    """Save data to a file with thread-safe locking."""
    try:
        if hasattr(data, "to_dict"):
            data = data.to_dict()  # Use to_dict if the object supports it

    
        if hasattr(data, "to_list"):
            data = data.to_list()  # Convert to a list if the object supports it

        with file_lock:  # Lock the file during the save operation
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
        print(f"Data successfully saved to {filename}")
    except Exception as e:
        print(f"Error saving to file {filename}: {e}")

def load_data_from_file(filename, data_type):
    """Load data from a file with thread-safe locking."""
    try:
        with file_lock:  # Lock the file during the load operation
            with open(filename, 'r') as f:
                data = json.load(f)

        if hasattr(data_type, "from_dict"):
            return data_type.from_dict(data)  # Use from_dict if the class supports it
        
        if hasattr(data_type, "from_list"):
            return data_type.from_list(data)  # Use from_list if the class supports it

        return data  # Return raw data for other types
    except json.JSONDecodeError:
        print(f"Error loading file {filename}: File is empty or contains invalid JSON. Reinitializing with default {data_type}.")
        default_data = data_type() if callable(data_type) else {}
        save_data_to_file(default_data, filename)
        return default_data
    except FileNotFoundError:
        print(f"{filename} not found. Creating a new file with default {data_type}.")
        default_data = data_type() if callable(data_type) else {}
        save_data_to_file(default_data, filename)
        return default_data
    except Exception as e:
        print(f"Unexpected error loading file {filename}: {e}")
        return None

