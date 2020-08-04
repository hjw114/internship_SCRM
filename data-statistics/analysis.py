import reader
import pandas as pd
import pymysql
import reader

def analysis(data_sql):
    thing = []
    data = {}
    for i in data_sql:
        for j in i:
            if (type(j) != float):
                if j in thing:
                    data[j] += 1
                else:
                    data[j] = 1
                    thing.append(j)
    return data


def save(dict):
    file_name = 'analysis.csv'
    df = pd.DataFrame.from_dict(dict,orient='index')
    df.columns = ["number"]
    df.sort_values("number", inplace=True, ascending=False)
    try:
        df.to_csv(file_name)
    except UnicodeEncodeError:
        print("编码错误, 该数据无法写到文件中, 直接忽略该数据")

def save_sql(dict):
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    for key in dict:
        cursor.execute("insert into goods_number values(%d','%d')" % (key, dict[key]))
    db.commit()
    db.close()
    cursor.close()  # 关闭

if __name__ == '__main__':
    idlist, goodslist = reader.search()
    save_sql(analysis(reader.data_handle(idlist, goodslist)))