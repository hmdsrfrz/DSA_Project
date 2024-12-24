# pricing.py
from save_load import save_data_to_file, load_data_from_file

class Pricing:
    def __init__(self, base_rate=10, per_km_rate=5, rideshare_discount=0.2, surge_multiplier=1.0, file_path='pricing.json'):
        self.file_path = file_path
        data = load_data_from_file(self.file_path, dict) or {}
        self.base_rate = data.get('base_rate', base_rate)
        self.per_km_rate = data.get('per_km_rate', per_km_rate)
        self.rideshare_discount = data.get('rideshare_discount', rideshare_discount)
        self.surge_multiplier = data.get('surge_multiplier', surge_multiplier)

    def save_to_file(self):
        data = {
            'base_rate': self.base_rate,
            'per_km_rate': self.per_km_rate,
            'rideshare_discount': self.rideshare_discount,
            'surge_multiplier': self.surge_multiplier,
        }
        save_data_to_file(data, self.file_path)

    
    def calculate_fare(self, distance, is_rideshare=False, is_peak_time=False):
        """
        Calculates the fare for a given distance, with options for ridesharing and peak time pricing.
        """
        fare = self.base_rate + (distance * self.per_km_rate)
        if is_rideshare:
            fare *= (1 - self.rideshare_discount)
        if is_peak_time:
            fare *= self.surge_multiplier
        return round(fare, 2)

    def split_fare(self, total_fare, num_passengers):
        """
        Splits the fare among rideshare participants.
        """
        if num_passengers <= 0:
            return total_fare
        return round(total_fare / num_passengers, 2)