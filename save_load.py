import json
import os
import threading
from data_structures import DoublyLinkedList, HashTable



# Custom encoder to handle non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'to_dict'):
            return obj.to_dict()  # Convert objects with 'to_dict()' method
        if hasattr(obj, 'to_list'):
            return obj.to_list()  # Convert LinkedList to list
        return super().default(obj)  # Fallback for unsupported objects

# Universal save function
def save_data_to_file(data, filename):
    try:
        if isinstance(data, Queue):
            data = list(data.queue)  # Convert Queue to list
        elif isinstance(data, PriorityQueue):
            data = [(priority, item) for priority, item in data.items()]
        elif isinstance(data, HashTable):
            data = data.to_dict()

        with open(filename, 'w') as f:
            json.dump(data, f, indent=4, cls=CustomJSONEncoder)
        return True
    except Exception as e:
        print(f"Error saving to {filename}: {e}")
        return False


# Universal load function with data type handling
def load_data_from_file(filename, data_type=dict):
    try:
        if not isinstance(filename, str):
            raise TypeError("Filename must be a string.")
        
        # Check if the file exists and is not empty
        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            print(f"File {filename} is empty or does not exist. Returning empty {data_type.__name__}.")
            return data_type()

        with open(filename, 'r') as f:
            data = json.load(f)

        # Convert to appropriate data structure
        if data_type == HashTable:
            if isinstance(data, dict):
                return HashTable.from_dict(data)
            else:
                print(f"Warning: Data from {filename} is not a dict. Initializing empty HashTable.")
                return HashTable()
        
        elif data_type == DoublyLinkedList:
            if isinstance(data, list):
                return DoublyLinkedList.from_list(data)
            else:
                print(f"Warning: Data from {filename} is not a list. Initializing empty DoublyLinkedList.")
                return DoublyLinkedList()

        return data  # Fallback for general dict/list cases

    except json.JSONDecodeError:
        print(f"JSON decode error in {filename}: File is likely empty or corrupted.")
        return data_type()  # Return an empty structure on error

    except Exception as e:
        print(f"Unexpected error loading {filename}: {e}")
        return data_type()
