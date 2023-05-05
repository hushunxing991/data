# 导入pandas包

import pandas as pd

# 导入jieba库

import jieba

# 导入collections包

from collections import Counter

# 读取数据

# 打开data.csv文件并将ip和评论数据显示
data = pd.read_csv('data.csv')
# 通过切片把评论切取出来

data1 = data.iloc[:, 0]
ip = data.iloc[:, -1]
# 将数据框转化为文本内容


data1.to_csv('data.txt', index=False, sep=',', encoding='utf_8_sig')
ip.to_csv('ip1.txt', index=False, sep=',', encoding='utf_8_sig')

# 读取文本内容

report = open('data.txt', encoding='utf_8').read()
file = open('ip1.txt', "r", encoding='utf_8')  # 以只读模式读取文件
lines = []
for i in file:
    lines.append(i)  # 逐行将文本存入列表lines中
file.close()
print(lines)
new = []
for line in lines:  # 逐行遍历
    p = 0  # 定义计数指针
    for bit in line:  # 对每行进行逐个字遍历
        if bit == '·':  # 遇到.时进行处理（我们可以修改成我们想要的定位）
            new.append(line[p + 1:])  #
            break  # 处理完一行后跳出当前循环
        else:
            p = p + 1

# jieba库中的cut进行分词

words = jieba.cut(report)
words1 = []
stopwords = set()
with open('停用词.txt', 'r', encoding='utf-8') as fr:
    for i in fr:
        stopwords.add(i.strip())
for i in words:
    if i not in stopwords:
        words1.append(i)
print(words)
# 通过for循环语句提取长度大于等于3个字的词
report_words = []

for word in words1:

    if len(word) >= 2:  # 将长度大于等于3个字的词放入列表

        report_words.append(word)

print(report_words)  # 输出

# 词频统计

# 获取词频最高的100个词

t = Counter(report_words).most_common(100)  # 取最多的100组

print(t)  #

# 导入相关库

from wordcloud import WordCloud
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

# 列表转换成字符串
content = ','.join(report_words)
font = r'C:\Windows\Fonts\simhei.TTF'  # 电脑自带的字体，黑体
stopword = ['']  # 设置停止词，也就是你不想显示的词
# img = Image.open(path+r'\background.png') #打开背景图片
# img_array = np.array(img) #将图片装换为数组

w = WordCloud(
    background_color='white',
    width=1000,
    height=800,
    # mask=img_array,  # 设置背景图片
    font_path=font,
    stopwords=stopword
).generate(content)  # 绘制词云图
plt.imshow(w)
plt.axis('off')  # 隐藏坐标轴
plt.show()  # 显示图片
w.to_file('词云图.png')  # 保存图片
