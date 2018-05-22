# -*- coding:utf-8 -*-
import json
from collections import defaultdict, OrderedDict
import jieba
from gensim import corpora
from streamparse import Bolt
project_path = '/Users/jason_lee/Documents/danmu_analysis'  # add abs path in order to file set file


class DanMuBolt(Bolt):

    def initialize(self, conf, ctx):
        self.interval_minute = 5
        self.danmu_array = []
        self.start_time = None
        with open(project_path + '/stopwords2.txt', 'rb') as f1:
            words = f1.readlines()
        self.stoplist = map(lambda x: x.strip().decode('utf-8'), words)

    def _analysis(self):
        corpus = map(lambda x: " ".join(jieba.cut(x, cut_all=False)), self.danmu_array)
        texts = [[word for word in document.lower().split() if word not in self.stoplist]
                 for document in corpus]
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1

        # Only keep words that appear more than once
        processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
        # print processed_corpus
        dictionary = corpora.Dictionary(processed_corpus)
        result = OrderedDict(sorted(dictionary.iteritems(), key=lambda x: x[0]))
        self.danmu_array = []
        with open(project_path + "/result.txt", 'a') as f:
            f.write('%s\n' % result)
        return result

    def process(self, tup):
        data = json.loads(tup.values[0])
        self.danmu_array.append(data['content'])
        # print data['level'], data['nickname']
        if not self.start_time:
            self.start_time = data['create_time']

        if data['create_time'] - self.start_time >= self.interval_minute * 60:
            self.start_time = data['create_time']
            analysis_result = self._analysis()
            self.emit([analysis_result])
