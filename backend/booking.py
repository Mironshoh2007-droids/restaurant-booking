import random
import string

class BookingManager:
    def __init__(self):
        self.bookings = []
        self.next_id = 1

    @staticmethod
    def generate_code():
        return ''.join(random.choices(string.digits, k=6))

    def create_booking(self, table_id, customer_name, date, time):
        code = self.generate_code()
        booking = {
            'id': self.next_id,
            'table_id': table_id,
            'customer_name': customer_name,
            'date': date,
            'time': time,
            'status': 'pending',
            'code': code
        }
        self.bookings.append(booking)
        self.next_id += 1
        return booking

    def cancel_booking(self, booking_id):
        for booking in self.bookings:
            if booking['id'] == booking_id:
                booking['status'] = 'cancelled'
                return True
        return False

    def cancel_by_code(self, code):
        for booking in self.bookings:
            if booking.get('code') == code and booking['status'] in ('pending', 'confirmed'):
                booking['status'] = 'cancelled'
                return True, booking
        return False, None

    def get_booked_table_ids(self, date, time):
        booked = []
        for b in self.bookings:
            if b.get('date') == date and b.get('time') == time and b.get('status') in ('pending', 'confirmed'):
                booked.append(b.get('table_id'))
        return booked