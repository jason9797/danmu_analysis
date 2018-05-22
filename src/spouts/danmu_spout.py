# -*- coding: utf-8 -*-
from streamparse import Spout
from confluent_kafka import Consumer


class DanMuSpout(Spout):
    outputs = ['word']

    def initialize(self, stormconf, context):
        broker = 'localhost:9092'
        group = 'test.py'
        conf = {'bootstrap.servers': broker, 'group.id': group, 'session.timeout.ms': 6000,
                'default.topic.config': {'auto.offset.reset': 'smallest'}}
        self.consumer = Consumer(**conf)

    def activate(self):
        self.consumer.subscribe(['danmu'])

    def next_tuple(self):
        msg = self.consumer.poll()
        if msg.value():
            self.emit([msg.value()])

    def deactivate(self):
        self.consumer.close()
