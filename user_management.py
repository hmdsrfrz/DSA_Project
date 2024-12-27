from data_structures import HashTable, DoublyLinkedList
from save_load import save_data_to_file, load_data_from_file
import uuid

class UserManagement:
    def __init__(self):
        # Load users from file or initialize an empty HashTable
        self.users = load_data_from_file('users_data.json', HashTable)
        self.active_sessions = HashTable()  # Active sessions are temporary and not loaded

    def register_user(self, name, email, phone, password):
        user_id = str(uuid.uuid4())
        user_data = {
            'id': user_id,
            'name': name,
            'email': email,
            'phone': phone,
            'password': password,  # In real system, this should be hashed
            'ride_history': DoublyLinkedList(),
            'active_ride': None
        }

        if self.get_user_by_email(email):
            return False, "Email already registered"

        self.users.insert(user_id, user_data)

        # Save to file immediately
        self.users.save_to_file('users_data.json')
        return True, user_id

    def login_user(self, email, password):
        print("Debug: Users table contents:", self.users.table)  # Debug statement
        for bucket in self.users.table.values():
            print("Debug: Current bucket:", bucket)  # Debug statement
            if bucket:  # Ensure the bucket is not empty
                for key, user_data in bucket:
                    print("Debug: Checking user_data:", user_data)  # Debug statement
                    if isinstance(user_data, dict) and user_data.get('email') == email and user_data.get('password') == password:
                        session_id = str(uuid.uuid4())  # Generate a session ID
                        self.active_sessions.insert(session_id, user_data['id'])  # Map session ID to user ID
                        return True, session_id  # Return the session ID
        print("Active Sessions:", self.active_sessions.table)
        return False, "Invalid credentials"
   
    '''def get_user_by_id(self, user_id):
        # Check if the provided user_id is a session ID
        original_user_id = self.active_sessions.get(user_id)
        if original_user_id:
            return self.users.get(original_user_id)
        return None  # Return None if neither session ID nor original user ID is found'''
    
    def get_user_by_id(self, user_id):
        """Get user by either their direct user ID or session ID."""
        print(f"Debug: Looking up user with ID: {user_id}")
        print(f"Debug: Current users in HashTable: {self.users.to_dict()}")
        
        # First try to get user directly from users table
        user = self.users.get(user_id)
        print(f"Debug: Direct user lookup result: {user}")
        
        if user:
            return user
            
        # If not found, check if it's a session ID
        original_user_id = self.active_sessions.get(user_id)
        print(f"Debug: Session lookup result: {original_user_id}")
        
        if original_user_id:
            return self.users.get(original_user_id)
            
        return None


    def get_user_by_email(self, email):
        for user_data in self.users.values():  # Use values() to get all user data
            if user_data['email'] == email:
                return user_data
        return None

    def update_user_profile(self, user_id, updates):
        user_data = self.users.get(user_id)
        if user_data:
            user_data.update(updates)
            self.users.insert(user_id, user_data)
            # Save updated data
            self.users.save_to_file('users_data.json')
            return True
        return False
