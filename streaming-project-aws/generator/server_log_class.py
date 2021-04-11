# Create a class for server logs
class ServerLog:
    def __init__(self, event_id, account_id, event_type, device, location_country, event_timestamp):
        self.event_id = event_id
        self.account_id = account_id
        self.event_type = event_type
        self.device = device
        self.location_country = location_country
        self.event_timestamp = event_timestamp

# We will utilize this method to send logs as dicts
    def to_dict(self):
        return {'event_id': self.event_id,
                'account_id': self.account_id,
                'event_type': self.event_type,
                'device': self.device,
                'location_country': self.location_country,
                'event_timestamp': self.event_timestamp}
