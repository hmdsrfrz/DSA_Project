import os
import json


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        # Add custom serialization logic if needed
        return super().default(obj)

def save_data_to_file(data, filename):
    """
    Saves data to a JSON file, handling specific data structure conversions.

    Args:
        data: The data to save (e.g., Queue, HashTable, Graph).
        filename: The name of the file to save the data to.

    Returns:
        True if successful, False otherwise.
    """
    from data_structures import DoublyLinkedList, HashTable, Queue, PriorityQueue, Graph
    try:

            # Convert specific data structures to serializable formats
            if isinstance(data, Queue):
                serializable_data = list(data.queue)
            elif isinstance(data, PriorityQueue):
                serializable_data = [(priority, item) for priority, item in data.items()]
            elif isinstance(data, HashTable):
                serializable_data = data.to_dict()
            elif isinstance(data, Graph):
                serializable_data = data.to_dict()
            elif isinstance(data, list):
                serializable_data = list(data)  # Create a copy of the list
            elif isinstance(data, dict):
                serializable_data = dict(data)  # Create a copy of the dict
            else:
                serializable_data = data

            # Save to JSON
            with open(filename, 'w') as f:
                json.dump(serializable_data, f, indent=4, cls=CustomJSONEncoder)
            return True
    except Exception as e:
            print(f"Error saving to {filename}: {e}")
            return False

def load_data_from_file(filename, data_type=dict):
    """
    Loads data from a JSON file, converting it to the specified data type.

    Args:
        filename: The name of the file to load data from.
        data_type: The expected type of the data (e.g., HashTable, Graph).

    Returns:
        An instance of the specified data_type or an empty instance if loading fails.
    """
    from data_structures import DoublyLinkedList, HashTable, Queue, PriorityQueue, Graph
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

        elif data_type == Graph:
            if isinstance(data, dict):
                return Graph.from_dict(data)  # Convert dictionary back to Graph
            else:
                print(f"Warning: Data from {filename} is not a dict. Initializing empty Graph.")
                return Graph()

        return data  # Fallback for general dict/list cases

    except json.JSONDecodeError:
        print(f"JSON decode error in {filename}: File is likely empty or corrupted.")
        return data_type()  # Return an empty structure on error

    except Exception as e:
        print(f"Unexpected error loading {filename}: {e}")
        return data_type()
