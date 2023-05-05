import re
import time
from datetime import datetime


def beforeHours2Date(hours, date_format='%Y-%m-%d %H:%M:%S'):
    hours = int(hours)
    t = time.time() - hours * 60 * 60
    t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t))
    return t

'''def beforeHours2Date1(hours, date_format='%Y-%m-%d %H:%M:%S'):
    hours = int(hours)
    t = time.time() - hours * 60 * 60
    t = time.strftime('%Y-%m-%d', time.localtime(t))
    return t'''



def parse_ymd(s):
    aa = re.findall(r"(\d{4}-\d{1,2}-\d{1,2}\s\d{1,2}:\d{1,2})", s)
    if '前天' in s:
        a = 2
        a = a * 24
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')

    if '天前' in s:
        a = s[0]
        a = int(a)
        a = a*24
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')

    if '周前' in s:
        b = s[0]
        b = int(b)
        a = 7 * b
        a *= 24
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')

    if '小时前' in s:
        a = re.findall('(.*?)小时前', s)
        a = beforeHours2Date(a[0], date_format='%Y-%m-%d %H:%M:%S')

    if '昨天' in s:
        a = 24
        b = re.findall('昨天 (.*)', s)
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')

    if '分钟前' in s:
        a = 0.5
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')

    if '刚刚' in s:
        a = 0
        a = beforeHours2Date(a, date_format='%Y-%m-%d %H:%M:%S')
    return a

