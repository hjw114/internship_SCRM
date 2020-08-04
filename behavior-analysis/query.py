import apriori
import pandas
import pymysql
import reader

def write_csv(data):
    file_name = 'conf.csv'
    save = pandas.DataFrame(data)
    save.columns =["freqSet - conseq","conseq","conf"]
    save.sort_values("conf",inplace=True,ascending=False)
    try:
        save.to_csv(file_name)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

def write_sql(sql_data):
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    for i in sql_data:
        for j in i:
            cursor.execute("insert into behavior_analysis_aprior values(%s','%s','%f')" % (i[0], i[1], i[2]))
    db.commit()
    db.close()

if __name__ == '__main__':
    idlist, goodslist = reader.search()
    dataSet = reader.data_handle(idlist, goodslist)
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    write_sql(rule)