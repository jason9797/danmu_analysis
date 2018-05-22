# -*- coding:utf-8 -*-
import time
import json
import confluent_kafka
from danmu import DanMuClient


def error_cb(err):
    print('Error: %s' % err)


dmc = DanMuClient('http://www.douyu.com/sunyalong')


@dmc.danmu
def produce(msg):
    """
    生产数据到broker
    :param msg: 弹幕数据
    :param producer:
    :return:
    """
    data = dict()
    data['content'] = msg['Content'].encode('utf-8', 'ignore')
    data['nickname'] = msg['NickName'].encode('utf-8', 'ignore')
    data['uid'] = msg['uid']
    data['level'] = msg['level']
    data['create_time'] = time.time()
    try:
        producer.produce('danmu', value=json.dumps(data))
        # time.sleep(random.randint(1, 2))
    except BufferError:
        producer.poll(100)


def main():
    global producer
    bootstrap_servers = 'localhost:9092'
    api_version_request = True
    conf = {'bootstrap.servers': bootstrap_servers,
            'api.version.request': api_version_request,
            'error_cb': error_cb,
            'debug': 'protocol',
            'broker.address.family': 'v4'}
    producer = confluent_kafka.Producer(**conf)
    dmc.start(blockThread=True)
    producer.flush()


if __name__ == '__main__':
    main()
