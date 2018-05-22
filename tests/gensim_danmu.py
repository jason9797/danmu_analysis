# encoding=utf-8
from collections import defaultdict
import jieba
from gensim import corpora
import json


with open('../../danmu.txt', 'rb') as f:
    messages = f.readlines()
    corpus = map(lambda x: " ".join(jieba.cut(x, cut_all=False)), messages)
    print corpus
    # Create a set of frequent words
    with open('../../stopwords2.txt', 'rb') as f1:
        words = f1.readlines()
        stoplist = map(lambda x: x.strip().decode('utf-8'), words)
    # print stoplist
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in corpus]
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # Only keep words that appear more than once
    processed_corpus = [[token for token in text if frequency[token] > 1] for text in texts]
    dictionary = corpora.Dictionary(processed_corpus)
    print sorted(dictionary.iteritems(), key=lambda x: x[0])
    # for key, value in dictionary.iteritems():
    #     print key, value

    # for message in messages:
    #     seg_list = jieba.cut(message, cut_all=True)
    #     print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    #
    #     seg_list = jieba.cut(message, cut_all=False)
    #     print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    #
    #     seg_list = jieba.cut(message)  # 默认是精确模式
    #     print(", ".join(seg_list))
    #
    #     seg_list = jieba.cut_for_search(message)  # 搜索引擎模式
    #     print(", ".join(seg_list))
