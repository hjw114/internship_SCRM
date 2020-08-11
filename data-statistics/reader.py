'''
本模块的功能为读取并初步分析数据库里的数据
author：胡觉文
'''
import pandas as pd
import numpy as np
import pymysql

def data_reader():#读取csv中数据
    data = pd.read_csv('data.csv')
    array_data = np.array(data)  # df数据转为np.ndarray()
    list_data = array_data.tolist()  # 将np.ndarray()转为列表
    for i in range(len(list_data)):
        list_data[i].remove(list_data[i][0])
    return list_data

def search():#读取并处理数据库中数据
    j = 0
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql1 = "SELECT goods_id FROM user_behavior "
    cursor.execute(sql1)
    goodslist = []
    allgoods = cursor.fetchall()  # 取出数据
    for s in allgoods:
        goodslist.append(s[0])
    sql2 = "SELECT times FROM user_behavior "
    cursor.execute(sql2)
    timelist = []
    alltime = cursor.fetchall()  # 取出数据
    for s in alltime:
        timelist.append(s[0].strftime('%m'))
    db.commit()
    db.close()
    cursor.close()  # 关闭
    for s in goodslist:#转换成种类
        goodslist[j] = int(s / 100)
        j = j + 1
    return goodslist,timelist

if __name__ == '__main__':
    #print(data_reader())
    goodslist,timelist=search()
    print(goodslist)
    print(timelist)