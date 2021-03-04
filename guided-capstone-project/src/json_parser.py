from datetime import datetime as d
import decimal
import json


def parse_json(line):
    res = []
    records = json.loads(line)
    try:  # check to see whether data dtypes are as expected in the row
        res.append(d.strptime(records["trade_dt"], '%m-%d-%Y').date())
        res.append(str(records["rec_type"]))
        res.append(str(records["symbol"]))
        res.append(str(records["exchange"]))
        res.append(str(records["execution_id"]) if records["execution_id"] else None)
        res.append(d.strptime(records["event_tm"], '%m-%d-%Y %H:%M'))
        res.append(int(records["event_seq_nb"]))
        res.append(d.strptime(records["arrival_tm"], '%m-%d-%Y %H:%M'))
        res.append(decimal.Decimal(records["trade_pr"]) if records["trade_pr"] else None)
        res.append(int(records["trade_size"]) if records["trade_size"] else None)
        res.append(decimal.Decimal(records["bid_pr"]) if records["bid_pr"] else None)
        res.append(int(records["bid_size"]) if records["bid_size"] else None)
        res.append(decimal.Decimal(records["ask_pr"]) if records["ask_pr"] else None)
        res.append(int(records["ask_size"]) if records["ask_size"] else None)
        if res[1] == 'T':            # check whether it is a trade record
            res.extend(['T', ''])
        elif res[1] == 'Q':          # check whether it is a quote record
            res.extend(['Q', ''])
        else:
            raise ValueError         # if there is an invalid event type, raise an error to catch it as bad record below
        return res
    except:
        # [save record to dummy event in bad partition]
        empty_record = [None for i in range(14)]  # create a list of null values
        bad = ['B', line]
        empty_record.extend(bad)                  # add bad partition key and the record (as one field) itself.
        return empty_record

