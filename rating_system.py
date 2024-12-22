# rating_system.py
class RatingSystem:
    def __init__(self, driver_management):
        self.driver_mgmt = driver_management
        
    def rate_driver(self, driver_id, rating):
        if rating < 1 or rating > 5:
            return False, "Rating must be between 1 and 5"
            
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        if not driver:
            return False, "Driver not found"
            
        # Update driver's rating
        total_ratings = driver['total_ratings']
        current_rating = driver['rating']
        
        new_total = total_ratings + 1
        new_rating = ((current_rating * total_ratings) + rating) / new_total
        
        driver['rating'] = round(new_rating, 2)
        driver['total_ratings'] = new_total
        
        self.driver_mgmt.drivers.insert(driver_id, driver)
        return True, driver['rating']
        
    def get_driver_rating(self, driver_id):
        driver = self.driver_mgmt.get_driver_by_id(driver_id)
        if driver:
            return True, {
                'rating': driver['rating'],
                'total_ratings': driver['total_ratings']
            }
        return False, "Driver not found"