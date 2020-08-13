'''
本模块实现购物行为数据处理储存功能
authon:胡觉文
弃用
'''
import apriori
import pandas
import pymysql
import reader

def write_csv(data):#写入csv
    file_name = 'conf.csv'
    save = pandas.DataFrame(data)
    save.columns =["freqSet - conseq","conseq","conf"]
    save.sort_values("conf",inplace=True,ascending=False)
    try:
        save.to_csv(file_name)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

def write_sql(sql_data):#写入sql
    freqSet_conseq = ""
    conseq = ""
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    for i in sql_data:
        cursor.execute("insert into behavior_analysis_aprior (freqSet_conseq,conseq,conf) values (%s,%s,%s)" % (i[0], i[1], i[2]))
    db.commit()
    db.close()

def delet():#删除数据库数据
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    cursor.execute("TRUNCATE TABLE behavior_analysis_aprior")
    db.commit()
    db.close()

if __name__ == '__main__':
    delet()
    idlist, goodslist,_ = reader.search()
    dataSet = reader.data_handle(idlist, goodslist)
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    write_sql(rule)