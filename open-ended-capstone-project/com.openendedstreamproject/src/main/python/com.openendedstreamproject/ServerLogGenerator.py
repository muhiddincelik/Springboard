from model.ServerLog import ServerLog
from multiprocessing import Pool
import random
import uuid
import datetime
import pandas as pd


class ServerLogGenerator(ServerLog):
    def __init__(self):
        self._random = random.random()
        self._location_country = ["US", "IN", "UK", "CA", "AU", "DE", "ES", "FR",
                                  "NL", "SG", "RU", "JP", "BR", "CN", "OT"]
        self._event_type = ["click", "purchase", "login", "log-out", "delete-account",
                            "create-account", "update-settings", "other"]
        self._columns = ['event_id', 'account_id', 'current_event_type', 'current_country', 'event_timestamp']

    def get_server_log(self):
        event_id = random.choices([uuid.uuid1(),'N/A',None,0],weights=[1000,1,1,1])[0]
        event_timestamp = random.choices([int(datetime.datetime.utcnow().timestamp()),
                                          datetime.datetime.utcnow().timestamp(),datetime.date.today(),
                                         'N/A',None,0],weights=[1000,1,1,1,1,1])[0]
        current_country = random.choices([self._location_country[random.randint(0, len(self._location_country) - 1)],
                                          'N/A',None,'unknown', 0], weights=[1000,1,1,1,1])[0]
        current_event_type = random.choices([self._event_type[random.randint(0, len(self._event_type) - 1)],
                                             'N/A',None,'---', 0], weights=[1000,1,1,1,1])[0]
        account_id = random.choices([random.randint(1, 10000), 'N/A',None, 0], weights=[1000,1,1,1])[0]
        super().__init__(event_id, account_id, current_event_type, current_country, event_timestamp)
        return self.to_list()

    def produce_log(self):
        list_of_rows = []
        i = 0
        while i < 200000:
            list_of_rows.append(self.get_server_log())
            i += 1
        df=pd.DataFrame(list_of_rows,columns=self._columns)
        df.to_csv(r'C:\Users\muhid\Desktop\log_data_10.csv', index=False)


if __name__ == "__main__":
    s = ServerLogGenerator()
    with Pool(processes=2, maxtasksperchild=1) as pool:
        multiple_results = [pool.apply_async(
            s.get_server_log()
        ) for i in range(10)]
        print('Running processes')
        for res in multiple_results:
            print(res)
