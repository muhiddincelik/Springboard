from model.ServerLog import ServerLog
from multiprocessing import Pool
import random
import uuid
import datetime
import pandas as pd
import json
from kafka import KafkaProducer
import time


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


class ServerLogGenerator(ServerLog):
    def __init__(self):
        self._random = random.random()
        self._location_country = ["US", "IN", "UK", "CA", "AU", "DE", "ES", "FR",
                                  "NL", "SG", "RU", "JP", "BR", "CN", "OT"]
        self._event_type = ["click", "purchase", "login", "log-out", "delete-account",
                            "create-account", "update-settings", "other"]
        self._columns = ['event_id', 'account_id', 'current_event_type', 'current_country', 'event_timestamp']

    def get_server_log(self):
        event_id = random.choices([uuid.uuid1(),'N/A',None,0],weights=[1,1,1,1])[0]
        event_timestamp = random.choices([int(datetime.datetime.utcnow().timestamp()),
                                          datetime.date.today().isoformat(),
                                         'N/A', None, 0], weights=[1,1,1,1,1])[0]
        current_country = random.choices([self._location_country[random.randint(0, len(self._location_country) - 1)],
                                          'N/A', None, 'unknown', 0], weights=[1,1,1,1,1])[0]
        current_event_type = random.choices([self._event_type[random.randint(0, len(self._event_type) - 1)],
                                             'N/A', None, '---', 0], weights=[1,1,1,1,1])[0]
        account_id = random.choices([random.randint(1, 10000), 'N/A',None, 0], weights=[1,1,1,1])[0]
        super().__init__(event_id, account_id, current_event_type, current_country, event_timestamp)
        return self.to_dict()

    # def produce_log(self):
    #     list_of_rows = []
    #     i = 0
    #     while i < 200000:
    #         list_of_rows.append(self.get_server_log())
    #         i += 1
    #     df=pd.DataFrame(list_of_rows,columns=self._columns)
    #     df.to_csv(r'C:\Users\muhid\Desktop\log_data_10.csv', index=False)


if __name__ == "__main__":
    producer = KafkaProducer(
                             bootstrap_servers=['localhost:9092'],
                             value_serializer=lambda x:
                             json.dumps(x, cls=UUIDEncoder).encode('utf-8'))
    #
    s = ServerLogGenerator()
    for i in range(2000):
        producer.send('logs', value=s.get_server_log())
        print(f'sending {i} record!')
        time.sleep(3)

    # with Pool(processes=2, maxtasksperchild=1) as pool:
    #     multiple_results = [pool.apply_async(
    #         s.get_server_log()
    #     ) for i in range(10)]
    #
    #     for res in multiple_results:
    #         producer.send('test', value=res.get())
    #         time.sleep(0.01)

    producer.close()
