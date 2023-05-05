from pyecharts.globals import ThemeType
from snownlp import SnowNLP  # 导入snownlp包

# 导入pandas包
import pltime
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map, Bar, Pie
# 导入plt函数，进行可视化

import matplotlib.pyplot as plt

# 导入样例数据

data = 'data.csv'

# 读取文本数据

df = pd.read_csv(data)

# 提取所有数据
# 提取评论和ip和评论时间
df1 = df.iloc[:, 0]
ip1 = df.iloc[:, -1]

print('将提取的数据打印出来：\n', df1, ip1)

# 遍历每条评论进行预测
# 调用Snownlp训练好的模型对每条评论进行预测，返回情感得分
values = [SnowNLP(i).sentiments for i in df1]

# 输出积极的概率，大于0.5积极的，小于0.5消极的
# myval保存预测值
myval = []

# 存放正面

good = 0

# 存放负面

bad = 0

for i in values:
    if i >= 0.5:  # 正面评价

        myval.append("有意向")

        good = good + 1

    else:  # 负面评价

        myval.append("无意向")

        bad = bad + 1

# 将数据框转化为文本内容

ip1.to_csv('ip_time.txt', index=False, sep=',', encoding='utf_8_sig')

# 读取文本内容

file = open('ip_time.txt', "r", encoding='utf_8')  # 以只读模式读取文件
lines = []
for i in file:
    lines.append(i)  # 逐行将文本存入列表lines中
file.close()
ip = []
time = []
for line in lines:  # 逐行遍历
    p = 0  # 定义计数指针
    for bit in line:  # 对每行进行逐个字遍历
        if bit == '·':  # 遇到.时进行处理，即遇到.后即为ip地址
            ip.append(line[p + 1:-1])  # 将line中的p + 1到末尾的字段存入新列表new中，用于写入新的.txt中
            time.append(line[0:p])
            break  # 处理完一行后跳出当前循环
        else:
            p = p + 1
print(ip)

plsjian = []
for i in range(len(time)):
    time1 = pltime.parse_ymd(time[i])
    plsjian.append(time1)
print(plsjian)
# 写入文件
df['预测值'] = values
df['评价类别'] = myval
df['ip地址'] = ip
df['评论时间'] = plsjian
# 将结果输出到csv
df_sort = df.sort_values(by='评价类别')  # 使用sort_values方法根据评价类别进行排序
df_sort.to_csv('snow_data.csv')  # 写入snow_data.csv文件，在运行的时候如果出现报错将这个文件改名，以及下方的read_csv的也一起修改
rate = good / (good + bad)

print('有意向购买率', '%.f%%' % (rate * 100))  # 格式化为百分比
# 调用read_csv和read_excel方法打开文件
text = pd.read_csv('snow_data.csv')
xls = pd.read_excel('sjileibie.xlsx')
counts = 0
for j in range(len(text.iloc[:, -1])):
    # 将预测的类别和实际类别进行比较，如何一样则认为正确，正确数counts+1
    if text.iloc[j, -3] == xls.iloc[j, -1]:
        counts += 1
# 输出本次预测的准确率，len（text）为求总得行数即有多少条数据
print(counts)
pre = (float(counts) / float(len(text)))
print(u"准确率为:"'%.f%%' % (pre * 100))


def address():
    add = pd.read_csv('snow_data.csv')

    add1 = add.iloc[:, -2]
    add2 = add.iloc[:, -3]
    s = set(add1)
    s.remove('美国')
    s.remove('柬埔寨')
    s.remove('IP未知')
    a = pd.DataFrame(s)
    a.to_csv('shenfen.csv')
    province = pd.read_csv('shenfen.csv')
    province1 = province.iloc[:, 1]
    count = [0] * 30
    dict1 = dict(zip(province1, count))
    for i in range(len(add1)):
        for j in dict1:
            if add1[i] == j and add2[i] == '有意向':
                dict1[j] += 1
    print(dict1)
    return dict1


# 作图

y = values


def wordc():
    y = values
    plt.rc('font', family='SimHei', size=10)  # 字体为自带的黑体显示

    plt.plot(y, marker='o', mec='r', mfc='w', label=u'评价分值')  # 图像类别显示y轴数据，圆点显示，红色，线为色

    plt.xlabel('用户')  # x轴

    plt.ylabel('评价分值')  # y轴

    # 让图例生效

    plt.legend()

    # 添加标题

    plt.title('评论情感分析', family='SimHei', size=14, color='black')
    plt.savefig('折线图.png')
    plt.show()


def createmap():
    dict1 = address()
    province1 = list(dict1.keys())
    count = list(dict1.values())
    ccc = {'山西': '山西省', '海南': '海南省', '陕西': '陕西省', '浙江': '浙江省', '江西': '江西省', '福建': '福建省', '宁夏': '宁夏回族自治区', '甘肃': '甘肃省',
           '重庆': '重庆市', '河北': '河北省', '黑龙江': '黑龙江省', '内蒙古': '内蒙古自治区', '上海': '上海市', '新疆': '新疆维吾尔自治区', '四川': '四川省',
           '北京': '北京市', '青海': '青海省', '广东': '广东省', '辽宁': '辽宁省',
           '湖南': '湖南省', '吉林': '吉林省', '云南': '云南省', '河南': '河南省', '江苏': '江苏省', '广西': '广西壮族自治区', '山东': '山东省', '贵州': '贵州省',
           '安徽': '安徽省', '西藏': '西藏自治区',
           '湖北': '湖北省', '天津': '天津市'}

    province = [ccc[i] if i in ccc else i for i in province1]
    a = [tuple(z) for z in zip(province, count)]
    print(a)
    c = (
        Map()
            .add("", data_pair=a, maptype="china", is_map_symbol_show=True, )
            .set_global_opts(title_opts=opts.TitleOpts(title="Map"),
                             visualmap_opts=opts.VisualMapOpts(max_=80, is_piecewise=True))

    )
    c.render("1.html")


def bar():
    s = pd.read_csv("snow_data.csv")
    data = s.sort_values(by="点赞数", ascending=False)
    # 把新的数据写入文件
    data.to_csv('点赞.csv', mode='w+', index=False)
    d = pd.read_csv("点赞.csv")
    comment = d.iloc[0:10, 1]
    print(comment)
    dianzan_count = d.iloc[0:10, 2]
    l1 = []
    y_value = [int(i) for i in dianzan_count]
    for i in comment:
        l1.append(i)

    print(type(l1))
    c = (
        Bar(init_opts=opts.InitOpts(width="1800px",
                                    height="700px",
                                    page_title="点赞前十评论",
                                    theme=ThemeType.MACARONS))
            .add_xaxis(l1)
            .add_yaxis("点赞数", y_value)
            .set_global_opts(
            xaxis_opts=opts.AxisOpts(name_rotate=60,
                                     axislabel_opts={"rotate": 45, "is_datazoom_show": True, "interval": 0})
            , title_opts={"text": "点赞数前十的评论", "subtext": " ",
                          }

        )
    )
    c.render("点赞数前十.html")


def pie():
    x = pd.read_excel('sjileibie.xlsx')
    x1 = x.iloc[:, -1]
    x2 = set(x1)
    count = [0] * 2
    for i in x1:
        if i == "有意向":
            count[0] += 1
        else:
            count[1] += 1
    print(count)
    c = (
        Pie()
            .add("", [list(z) for z in zip(x2, count)])
            .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple"])
            .set_global_opts(title_opts=opts.TitleOpts(title="Pie-设置颜色"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
            .render("pie_set_color.html")
    )


def pie1():
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
    c.render("accuracy.html")


if __name__ == '__main__':
    address()
    wordc()
    createmap()
    bar()
    pie()
    pie1()
