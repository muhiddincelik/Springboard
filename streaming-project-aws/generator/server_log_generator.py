from generator.server_log_class import ServerLog
import datetime
import random
import uuid
import pytz


# Create a log generator using log class we created
class ServerLogGenerator(ServerLog):
    def __init__(self):
        self._random = random.random()
        self._location_country = ["US", "IN", "UK", "CA", "AU", "DE", "ES", "FR",
                                 "NL", "SG", "RU", "JP", "BR", "CN", "OT"]
        self._event_type = ["click", "purchase", "login", "log-out", "delete-account",
                           "create-account", "update-settings", "other"]
        self._columns = ['event_id', 'account_id', 'event_type', 'device', 'location_country', 'event_timestamp']

    # basically we introduce some random anomalies in logs with this method
    def get_server_log(self):
        event_id = random.choices([uuid.uuid1(),
                                   'N/A',
                                   None,
                                   0],
                                  weights=[5, 0.01, 0.01, 0.01])[0]

        account_id = random.choices([random.randint(1, 1000),
                                     'N/A',
                                     None,
                                     random.randint(10001, 100000)],
                                    weights=[5, 0.01, 0.01, 0.01])[0]

        event_type = random.choices([self._event_type[random.randint(0, len(self._event_type) - 1)],
                                    'N/A',
                                     None,
                                     '---',
                                     0], weights=[5, 0.01, 0.01, 0.01, 0.01])[0]

        device = random.choices(['ANDROID',
                                 'IOS',
                                 None,
                                 'unknown'],
                                weights=[1, 0.08, 0.01, 0.01])[0]

        event_timestamp = random.choices([int(datetime.datetime.now(pytz.timezone("US/Pacific")).timestamp()),
                                          datetime.date.today().isoformat(),
                                         'N/A',
                                          None,
                                          0],
                                         weights=[4, 0.01, 0.01, 0.01, 0.01])[0]

        location_country = random.choices([self._location_country[random.randint(0, len(self._location_country) - 1)],
                                          'N/A',
                                           None,
                                           'unknown',
                                           0],
                                          weights=[5, 0.01, 0.01, 0.01, 0.01])[0]

        super().__init__(event_id, account_id, event_type, device, location_country, event_timestamp)

        # return instance attributes as dict
        return self.to_dict()


