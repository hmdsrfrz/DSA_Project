#data_structures.py
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
        if index > 0 and self.heap[index][0] < self.heap[parent][0]:  # Compare only priorities
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            self._heapify_up(parent)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:  # Compare only priorities
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:  # Compare only priorities
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
        distances, previous = self.dijkstra(start)
        if distances[end] == float('infinity'):
            return None  # No path exists

        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        return path  # Return only the path

        

    def get_shortest_path_distance(self, start, end):
        if start not in self.nodes or end not in self.nodes:
            return None
        distances, _ = self.dijkstra(start)
        return distances.get(end, float('inf'))



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
    
    def to_dict(self):
        """
        Converts the Graph into a dictionary for serialization.
        """
        return {"nodes": self.nodes}

    @classmethod
    def from_dict(cls, data):
        """
        Reconstructs a Graph from a dictionary.
        """
        new_graph = cls()
        new_graph.nodes = data.get("nodes", {})
        return new_graph

class DoublyLinkedList:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None

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

    def to_list(self):
        """Convert linked list to Python list"""
        result = []
        current = self.head
        while current:
            # Handle nested objects that might have to_dict or to_list methods
            if hasattr(current.data, 'to_dict'):
                result.append(current.data.to_dict())
            elif hasattr(current.data, 'to_list'):
                result.append(current.data.to_list())
            else:
                result.append(current.data)
            current = current.next
        return result

    def to_dict(self):
        """Convert to dictionary for JSON serialization compatibility"""
        return {'data': self.to_list()}

    @classmethod
    def from_list(cls, data_list):
        """Create linked list from Python list"""
        ll = cls()
        for item in data_list:
            # Handle dictionary input for nested objects
            if isinstance(item, dict):
                if 'data' in item and isinstance(item['data'], list):
                    # Handle nested LinkedList
                    ll.append(cls.from_list(item['data']))
                else:
                    # Handle nested HashTable
                    ll.append(HashTable.from_dict(item))
            else:
                ll.append(item)
        return ll
    
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
                return True
        return False

    def __str__(self):
        """String representation for debugging"""
        return f"DoublyLinkedList({self.to_list()})"

    def __eq__(self, other):
        """Enable equality comparison"""
        if not isinstance(other, DoublyLinkedList):
            return False
        return self.to_list() == other.to_list()
    
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]  # List of lists for chaining

    def _hash(self, key):
        """Compute the hash index for a key."""
        return hash(key) % self.size

    def insert(self, key, value):
        """Insert or update a key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)  # Update existing key
                return
        self.table[index].append((key, value))  # Add new key-value pair

    def get(self, key):
        """Retrieve value by key."""
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Delete a key-value pair."""
        index = self._hash(key)
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                del self.table[index][i]
                return True
        return False

    def values(self):
        """Return all values (dictionary-like)."""
        return [v for bucket in self.table for k, v in bucket]

    def items(self):
        """Return all key-value pairs."""
        return [(k, v) for bucket in self.table for k, v in bucket]

    def to_dict(self):
        """Convert to a dictionary for JSON serialization."""
        result = {}
        for bucket in self.table:
            for key, value in bucket:
                # Handle nested objects that might have to_dict method
                if hasattr(value, 'to_dict'):
                    result[str(key)] = value.to_dict()
                # Handle nested objects that might have to_list method
                elif hasattr(value, 'to_list'):
                    result[str(key)] = value.to_list()
                else:
                    result[str(key)] = value
        return result

    @classmethod
    def from_dict(cls, data_dict):
        """Create HashTable from dictionary"""
        ht = cls()
        # Clear the initial empty buckets
        ht.table = [[] for _ in range(ht.size)]
        # Insert each key-value pair using the existing insert method
        for key, value in data_dict.items():
            ht.insert(key, value)
        return ht

    def buckets(self):
        """Return raw table structure for iteration."""
        return self.table

    

    
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
    
    def to_dict(self):
        """
        Converts the Queue into a dictionary for serialization.
        """
        return {"queue": self.queue}

    @classmethod
    def from_dict(cls, data):
        """
        Reconstructs a Queue from a dictionary.
        """
        new_queue = cls()
        new_queue.queue = data.get("queue", [])
        return new_queue

class PriorityQueue(MinHeap):
    def __init__(self):
        super().__init__()

    def push(self, priority, item):
        super().push((priority, item))  # Push a tuple of (priority, item)

    def pop(self):
        return super().pop()[1] if self.heap else None  # Return only the item

    def peek(self):
        return self.heap[0][1] if self.heap else None  # Return only the item

    def to_dict(self):
        return {"heap": self.heap}
    
        
    def to_list(self):
        return [item for _, item in self.heap]  # Extract items from the heap



    @classmethod
    def from_dict(cls, data):
        new_pq = cls()
        new_pq.heap = data.get("heap", [])
        return new_pq
    
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
