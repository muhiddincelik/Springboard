

class ServerLog:
    def __init__(self, event_id, account_id, event_type, location_country, event_timestamp):
        self.event_id = event_id
        self.account_id = account_id
        self.event_type = event_type
        self.location_country = location_country
        self.event_timestamp = event_timestamp

    def to_dict(self):
        #return f"{self.event_id},{self.account_id},{self.event_type},{self.location_country},{self.event_timestamp}"
        return {'event_id': self.event_id, 'account_id': self.account_id, 'event_type': self.event_type,
                'location_country': self.location_country, 'event_timestamp': self.event_timestamp}

