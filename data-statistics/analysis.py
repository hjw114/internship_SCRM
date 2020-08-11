'''
本模块的主要功能为分析季节性和热点商品
author：胡觉文
'''
import pymysql
import reader

def analysis(goodslist,timelist):#分析热点和季节性商品
    thing = []
    spring = []
    summer = []
    autumn = []
    winter = []
    data = [{},{},{},{},{}]
    for i in goodslist:#分析热点商品
        if i in thing:
            data[0][i] += 1
        else:
            data[0][i] = 1
            thing.append(i)
    for s in range(len(goodslist)):#分析季节性商品
        if (timelist[s] == "03" or timelist[s] == "04" or timelist[s] == "05"):
            if goodslist[s] in spring:
                data[1][goodslist[s]] += 1
            else:
                data[1][goodslist[s]] = 1
                spring.append(goodslist[s])
        elif (timelist[s] == "06" or timelist[s] == "07" or timelist[s] == "08"):
            if goodslist[s] in summer:
                data[2][goodslist[s]] += 1
            else:
                data[2][goodslist[s]] = 1
                summer.append(goodslist[s])
        elif (timelist[s] == "09" or timelist[s] == "10" or timelist[s] == "11"):
            if goodslist[s] in autumn:
                data[3][goodslist[s]] += 1
            else:
                data[3][goodslist[s]] = 1
                autumn.append(goodslist[s])
        elif (timelist[s] == "12" or timelist[s] == "01" or timelist[s] == "02"):
            if goodslist[s] in winter:
                data[4][goodslist[s]] += 1
            else:
                data[4][goodslist[s]] = 1
                winter.append(goodslist[s])
    return data

def save_sql(dict):#存入数据库
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql1 = "insert into goods_number (goods_id,total,spring,summer,autumn,winter) values (%s,%s,%s,%s,%s,%s)"
    for key in dict[0]:
        cursor.execute(sql1, [key, dict[0][key], dict[1].setdefault(key, 0), dict[2].setdefault(key, 0),
                              dict[3].setdefault(key, 0), dict[4].setdefault(key, 0)])
    db.commit()
    db.close()
    cursor.close()  # 关闭

if __name__ == '__main__':
    goodslist, timelist = reader.search()
    dict = analysis(goodslist,timelist)
    print(dict)
    save_sql(dict)