from server_log_generator import ServerLogGenerator
from kafka import KafkaProducer
import time
import json
import uuid

# Declare broker and topic variables to use when sending records
kafka_broker = 'broker:9092'
kafka_producer_topic = 'server-logs'


# Utilize uuid module for encoding
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)


# Driver Code
if __name__ == "__main__":

    producer = KafkaProducer(
                             bootstrap_servers=kafka_broker,
                             value_serializer=lambda x:
                             json.dumps(x, cls=UUIDEncoder).encode('utf-8'))

    # Crete a ServerLogGenerator instance
    s = ServerLogGenerator()
    for i in range(1, 200000):
        record = s.get_server_log()                         # In each call, we will get a randomized log
        producer.send(kafka_producer_topic, value=record)
        print(f'sending record {i}: {record}')              # Debug
        time.sleep(10)                                      # Time to sleep to send the next log





