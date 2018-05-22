import sys

from danmu import DanMuClient


dmc = DanMuClient('http://www.douyu.com/sunyalong')


@dmc.danmu
def danmu_fn(msg):
    # level = msg['level']
    # uid = msg['uid']
    # message = '[%s] %s' % (msg['NickName'], msg['Content'])
    with open("danmu.txt", 'a') as f:
        f.write(msg['Content'].encode('utf-8', 'ignore') + '\n')
    # print message.encode(sys.stdin.encoding, 'ignore').decode(sys.stdin.encoding)


dmc.start(blockThread=True)
