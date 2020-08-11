'''
本模块的功能是读取数据库中用户行为数据
author：胡觉文
'''
import pandas as pd
import numpy as np
import pymysql

def data_reader():#csv搜索数据
    data = pd.read_csv('data.csv')
    array_data = np.array(data)  # df数据转为np.ndarray()
    list_data = array_data.tolist()  # 将np.ndarray()转为列表
    for i in range(len(list_data)):
        list_data[i].remove(list_data[i][0])
    return list_data

def search():#数据库搜索数据
    i = 0
    j = 0
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql1 = "SELECT users_id FROM user_behavior "
    cursor.execute(sql1)
    idlist = []
    allid = cursor.fetchall()  # 取出数据
    for s in allid:
        idlist.append(s[0])
    sql2 = "SELECT goods_id FROM user_behavior "
    cursor.execute(sql2)
    goodslist = []
    allgoods = cursor.fetchall()  # 取出数据
    for s in allgoods:
        goodslist.append(s[0])
    sql3 = "SELECT actions FROM user_behavior "
    cursor.execute(sql3)
    actionlist = []
    allaction = cursor.fetchall()  # 取出数据
    for s in allaction:
        actionlist.append(s[0])
    db.commit()
    db.close()
    cursor.close()  # 关闭
    return idlist,goodslist,actionlist

def data_handle(idlist,goodslist):#数据初步处理对应成列表
    i = 0
    j = 0
    list_data = []
    for s in goodslist:#取出产品类别
        goodslist[j] = int(s/100)
        j = j + 1
    for n in range(len(idlist)):#对应用户产品成列表
        if n != 0:
            if idlist[n] == idlist[n - 1]:
                list_data[i].append(goodslist[n])
            else:
                list_data.append([])
                i = i + 1
                list_data[i].append(goodslist[n])
        else:
            list_data.append([])
            list_data[0].append(goodslist[0])
    return list_data

if __name__ == '__main__':
    #print(data_reader())
    idlist,goodslist,_=search()
    print(data_handle(idlist,goodslist))