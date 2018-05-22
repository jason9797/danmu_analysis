#!/usr/bin/env python
import time
import json
from confluent_kafka import Consumer


def main():
    bootstrap_servers = 'localhost:9092'
    group = 'test.py'
    conf = {'bootstrap.servers': bootstrap_servers, 'group.id': group, 'session.timeout.ms': 6000,
            'default.topic.config': {'auto.offset.reset': 'smallest'}}
    consumer = Consumer(**conf)
    consumer.subscribe(['danmu'])
    while True:
        msg = consumer.poll()
        try:
            print json.loads(msg.value())
        except ValueError:
            time.sleep(1)
        continue
    consumer.close()

if __name__ == '__main__':
    main()