from collections import defaultdict
import os
import re
import jieba
import jieba.posseg
import codecs
import csv
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Pie
# 生成stopword表，需要去除一些否定词和程度词汇


'''stopwords = set()
fr = open('data/停用词.txt', 'r', encoding='utf-8')
for word in fr:
    stopwords.add(word.strip())  # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
# 读取否定词文件
not_word_file = open('data/否定词.txt', 'r+', encoding='utf-8')
not_word_list = not_word_file.readlines()
not_word_list = [w.strip() for w in not_word_list]
# 读取程度副词文件
degree_file = open('data/程度副词.txt', 'r+', encoding='utf-8')
degree_list = degree_file.readlines()
degree_list = [item.split(',')[0] for item in degree_list]
# 生成新的停用词表
with open('stopwords.txt', 'w', encoding='utf-8') as f:
    for word in stopwords:
        if (word not in not_word_list) and (word not in degree_list):
            f.write(word + '\n')


# jieba分词后去除停用词
def seg_word(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for i in seg_list:
        seg_result.append(i)
    print(seg_result)
    stopwords = set()
    with open('stopwords.txt', 'r', encoding='utf-8') as fr:
        for i in fr:
            stopwords.add(i.strip())
    return list(filter(lambda x: x not in stopwords, seg_result))


# 找出文本中的情感词、否定词和程度副词
def classify_words(word_list):
    # 读取情感词典文件
    sen_file = open('data/BosonNLP_sentiment_score.txt', 'r+', encoding='utf-8')
    # 获取词典文件内容
    sen_list = sen_file.readlines()
    # 创建情感字典
    sen_dict = defaultdict()
    # 读取词典每一行的内容，将其转换成字典对象，key为情感词，value为其对应的权重
    for i in sen_list:
        if len(i.split(' ')) == 2:
            sen_dict[i.split(' ')[0]] = i.split(' ')[1]

    # 读取否定词文件
    not_word_file = open('data/否定词.txt', 'r+', encoding='utf-8')
    not_word_list = not_word_file.readlines()
    # 读取程度副词文件
    degree_file = open('data/程度副词.txt', 'r+', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        degree_dict[i.split(',')[0]] = i.split(',')[1]

    sen_word = dict()
    not_word = dict()
    degree_word = dict()
    # 分类
    for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys() and word not in not_word_list and word not in degree_dict.keys():
            # 找出分词结果中在情感字典中的词
            sen_word[i] = sen_dict[word]
            print(sen_word)
        elif word in not_word_list and word not in degree_dict.keys():
            # 分词结果中在否定词列表中的词
            not_word[i] = -1
            print(not_word)
        elif word in degree_dict.keys():
            # 分词结果中在程度副词中的词
            degree_word[i] = degree_dict[word]
            print(degree_word)

    # 关闭打开的文件
    sen_file.close()
    not_word_file.close()
    degree_file.close()
    # 返回分类结果
    return sen_word, not_word, degree_word


# 计算情感词的分数
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    # 权重初始化为1
    W = 1
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    # 遍历分词结果
    for i in range(0, len(seg_result)):
        # 如果是情感词
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * float(sen_word[i])
            # 情感词下标加一，获取下一个情感词的位置
            sentiment_index += 1
            if sentiment_index < len(sentiment_index_list) - 1:
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，权重取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        W *= float(degree_word[j])
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score


# 计算得分
def sentiment_score(sentence):
    # 1.对文档分词
    seg_list = seg_word(sentence)
    # 2.将分词结果转换成字典，找出情感词、否定词和程度副词
    sen_word, not_word, degree_word = classify_words(seg_list)
    # 3.计算得分
    score = score_sentiment(sen_word, not_word, degree_word, seg_list)
    return score


import csv


def read_data(filename):
    data = []
    score = []
    with open(filename, 'r', encoding="utf8") as s:
        csv_reader = csv.reader(s)
        for row in csv_reader:
            data.append(row[0])
        for i in data:
            score.append(sentiment_score(i))
            print(sentiment_score(i))
    return score


def fenci(filename):
    data1 = []
    fenci = []
    biaoz = []
    with open('fenci1.txt', 'w', encoding='utf-8') as f:
        with open(filename, 'r', encoding="utf8") as s:
            csv_reader = csv.reader(s)
            for row in csv_reader:
                data1.append(row[0])
            for i in data1:
                fenci.append(seg_word(i))
                #biaoz.append(pos_sentence(i))
                f.write(str(seg_word(i)) + '\n')


# 词性标注
def pos_sentence(sentence):
    sentence_seged = jieba.posseg.cut(sentence)
    outstr = ''
    for x in sentence_seged:
        outstr += "{}/{}  ".format(x.word, x.flag)
    return outstr


def load_data(filename):
    score = read_data(filename)
    myval = []

    # 存放正面

    good = 0

    # 存放负面

    bad = 0

    for i in score:

        if (i >0 ):  # 正面评价

            myval.append("有意向")

            good = good + 1

        else:  # 负面评价

            myval.append("无意向")

            bad = bad + 1
    data = filename

    # 读取文本数据

    df = pd.read_csv(data)
    print(data)
    df['情感得分'] = score[1:]
    df['购买意向'] = myval[1:]
    df.to_csv('qgcd_data.csv')
    load_data('data.csv')
fenci('data.csv')'''

text = pd.read_csv('qgcd_data.csv')
xls = pd.read_excel('sjileibie.xlsx')
counts = 0
for j in range(len(text.iloc[:, -1])):
    # 将预测的类别和实际类别进行比较，如何一样则认为正确，正确数counts+1
    if text.iloc[j, -1] == xls.iloc[j, -1]:
        counts += 1
# 输出本次预测的准确率，len（text）为求总得行数即有多少条数据
pre = (float(counts) / float(len(text)))
print(u"准确率为:"'%.f%%' % (pre * 100))

a = [0] * 2
a[0] = counts
a[1] = len(text) - counts
b = ["预测准确", "预测错误"]
c = (
    Pie()
        .add("", [list(z) for z in zip(b, a)])
        .set_colors(["yellow", "red", "pink", "orange", "purple", "blue", "green"])
        .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))

)
c.render("accuracy2.html")