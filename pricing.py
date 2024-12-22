# pricing.py
class Pricing:
    def __init__(self, base_rate=10, per_km_rate=5, rideshare_discount=0.2, surge_multiplier=1.0):
        self.base_rate = base_rate
        self.per_km_rate = per_km_rate
        self.rideshare_discount = rideshare_discount
        self.surge_multiplier = surge_multiplier

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