# user_management.py
from data_structures import HashTable, DoublyLinkedList
import uuid

class UserManagement:
    def __init__(self):
        self.users = HashTable()  # Store user data
        self.active_sessions = HashTable()  # Track logged-in users
        self.users.load_from_file('users_data.json')
        
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
                        session_id = str(uuid.uuid4())
                        self.active_sessions.insert(session_id, user_data['id'])
                        return True, session_id
        return False, "Invalid credentials"





        
    def get_user_by_id(self, user_id):
        return self.users.get(user_id)
        
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
            return True
        return False