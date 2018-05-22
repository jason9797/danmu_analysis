"""
Word count topology
"""

from streamparse import Grouping, Topology

from bolts.danmu_bolt import DanMuBolt
from spouts.danmu_spout import DanMuSpout


class WordCount(Topology):
    danmu_spout = DanMuSpout.spec()
    danmu_analysis = DanMuBolt.spec(inputs=[danmu_spout])
