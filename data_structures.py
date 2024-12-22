import json

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, index):
        parent = (index - 1) // 2
        if index > 0 and self.heap[index] < self.heap[parent]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def peek(self):
        if self.heap:
            return self.heap[0]
        return None
    def is_empty(self):
        return len(self.heap) == 0

    def size(self):
        return len(self.heap)



class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, location):
        if location not in self.nodes:
            self.nodes[location] = {}

    def add_edge(self, start, end, distance):
        if start in self.nodes and end in self.nodes:
            self.nodes[start][end] = distance
            self.nodes[end][start] = distance  # Since it's an undirected graph

    def get_neighbors(self, node):
        return self.nodes.get(node, {})

    def dijkstra(self, start):
        """
        Implementation of Dijkstra's shortest path algorithm using MinHeap.
        
        Args:
            start: Starting node
            
        Returns:
            Dictionary of shortest distances to all nodes from start node
            Dictionary of previous nodes in the shortest path
        """
        # Initialize distances with infinity for all nodes except start
        distances = {node: float('infinity') for node in self.nodes}
        distances[start] = 0
        
        # Dictionary to store the previous node in shortest path
        previous = {node: None for node in self.nodes}
        
        # Create min heap for storing vertices to visit
        pq = MinHeap()
        pq.push((0, start))  # (distance, node)
        
        # Set to keep track of visited nodes
        visited = set()
        
        while not pq.is_empty():
            # Get the node with minimum distance
            current_distance, current_node = pq.pop()
            
            # If we've already processed this node, skip it
            if current_node in visited:
                continue
                
            # Mark node as visited
            visited.add(current_node)
            
            # If current distance is greater than known distance, skip
            if current_distance > distances[current_node]:
                continue
            
            # Check all neighbors of current node
            for neighbor, weight in self.nodes[current_node].items():
                # Skip if neighbor is already visited
                if neighbor in visited:
                    continue
                    
                # Calculate tentative distance to neighbor
                distance = current_distance + weight
                
                # If we found a shorter path, update it
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    pq.push((distance, neighbor))
        
        return distances, previous

    def get_shortest_path(self, start, end):
        """
        Gets the shortest path between start and end nodes.
        
        Args:
            start: Starting node
            end: Ending node
            
        Returns:
            tuple: (path_distance, path_nodes)
            where path_distance is the total distance
            and path_nodes is a list of nodes in the path
        """
        # Get shortest distances and previous nodes
        distances, previous = self.dijkstra(start)
        
        if distances[end] == float('infinity'):
            return None, None  # No path exists
            
        # Reconstruct the path
        path = []
        current = end
        
        while current is not None:
            path.append(current)
            current = previous[current]
            
        # Reverse path to get it from start to end
        path.reverse()
        
        return distances[end], path

    def get_all_paths(self, start):
        """
        Gets all shortest paths from start node to all other nodes.
        
        Args:
            start: Starting node
            
        Returns:
            Dictionary with end nodes as keys and (distance, path) tuples as values
        """
        distances, previous = self.dijkstra(start)
        paths = {}
        
        for end in self.nodes:
            if end == start:
                paths[end] = (0, [start])
                continue
                
            if distances[end] == float('infinity'):
                paths[end] = (None, None)
                continue
                
            # Reconstruct path
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = previous[current]
            path.reverse()
            
            paths[end] = (distances[end], path)
            
        return paths

class DoublyLinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None

    def to_list(self):
        """Convert the linked list into a list."""
        result = []
        current = self.head
        while current:
            result.append(current.data)  # Assuming each node has a 'data' attribute
            current = current.next
        return result

    @classmethod
    def from_list(cls, data_list):
        """Reconstruct the linked list from a list."""
        new_list = cls()
        for item in data_list:
            new_list.append(item)  # Assuming an `append` method exists
        return new_list

    def append(self, data):
        new_node = self.Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def traverse_forward(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def traverse_backward(self):
        current = self.tail
        while current:
            print(current.data)
            current = current.prev

    def delete(self, data):
        current = self.head
        while current:
            if current.data == data:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                return
            current = current.next

class HashTable:
    def __init__(self, size=10):  # Initialize with a default size
        self.table = {}  # Use a dictionary to store key-value pairs

    def hash_function(self, key):
        # Simple hash function (you can implement more sophisticated ones)
        hash_value = hash(key) % len(self.table) if self.table else 0
        return hash_value
    
    def save_to_file(self, filename):
        table_data = {}
        for bucket in self.table.values():
            if bucket:
                for key, value in bucket:
                    # Serialize DoublyLinkedList objects
                    serializable_value = value.copy()  # Copy the dictionary
                    if isinstance(value.get('ride_history'), DoublyLinkedList):
                        serializable_value['ride_history'] = value['ride_history'].to_list()
                    table_data[key] = serializable_value
        try:
            with open(filename, 'w') as f:
                json.dump(table_data, f, indent=4)
            print(f"Data successfully saved to {filename}")
        except Exception as e:
            print(f"Error saving to file {filename}: {e}")

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                print("Loaded users:", self.users)  # Debug statement
                for key, value in data.items():
                    # Deserialize DoublyLinkedList objects
                    if 'ride_history' in value:
                        value['ride_history'] = DoublyLinkedList.from_list(value['ride_history'])
                    self.insert(key, value)
            print(f"Data successfully loaded from {filename}")
        except FileNotFoundError:
            print(f"{filename} not found. Starting with an empty table.")
        except Exception as e:
            print(f"Error loading file {filename}: {e}")



    def insert(self, key, value):
        index = self.hash_function(key)
        if index not in self.table:
            self.table[index] = []
        self.table[index].append((key, value))  # Handle collisions by storing in list

    def get(self, key):
        index = self.hash_function(key)
        if index in self.table:
            for k, v in self.table[index]:
                if k == key:
                    return v
        return None

    def delete(self, key):
        index = self.hash_function(key)
        if index in self.table:
            for i, (k, v) in enumerate(self.table[index]):
                if k == key:
                    del self.table[index][i]
                    break

    def values(self):
        # Flatten the table and return all values
        return [value for bucket in self.table.values() for key, value in bucket]

    def items(self):
        # Flatten the table and return all key-value pairs
        return [(key, value) for bucket in self.table.values() for key, value in bucket]

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if self.queue:
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if self.queue:
            return self.queue[0]
        return None

class PriorityQueue(MinHeap):
    def __init__(self):
        super().__init__()

    def push(self, priority, item):
        super().push((priority, item))

    def pop(self):
        return super().pop()[1] if self.heap else None

    def peek(self):
        return self.heap[0][1] if self.heap else None

class AVLTree:
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.height = 1
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    # Implement AVL Tree methods (insert, delete, rotate, balance) as needed

# Additional data structures can be added here if necessary for the project requirements.
