import decimal
from datetime import datetime as d


def parse_csv(arr):
    records = arr.split(",")
    res = []
    try:  # check to see whether data dtypes are as expected in the row
        res.append(d.strptime(records[0], '%m-%d-%Y').date())
        res.append(str(records[1]))
        res.append(str(records[2]))
        res.append(str(records[3]))
        res.append(str(records[4]) if records[4] else None)
        res.append(d.strptime(records[5], '%m-%d-%Y %H:%M'))
        res.append(int(records[6]))
        res.append(d.strptime(records[7], '%m-%d-%Y %H:%M'))
        res.append(decimal.Decimal(records[8]) if records[8] else None)
        res.append(int(records[9]) if records[9] else None)
        res.append(decimal.Decimal(records[10]) if records[10] else None)
        res.append(int(records[11]) if records[11] else None)
        res.append(decimal.Decimal(records[12]) if records[12] else None)
        res.append(int(records[13]) if records[13] else None)
        if res[1] == 'T':            # check whether it is a trade record
            res.extend(['T', ''])
        elif res[1] == 'Q':          # check whether it is an exchange record
            res.extend(['Q', ''])
        else:
            raise ValueError         # if there is an invalid event type, raise an error to catch it as bad record below
        return res
    except:
        # [save record to dummy event in bad partition]
        empty_record = [None for i in range(14)]  # create a list of null values
        bad = ['B', arr]
        empty_record.extend(bad)                  # add bad partition key and the record (as one field) itself
        return empty_record

