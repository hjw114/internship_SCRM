import pandas as pd
import pymysql
import reader

def analysis_hot(goodslist,timelist):
    thing = []
    spring = []
    summer = []
    autumn = []
    winter = []
    data = [{},{},{},{},{}]
    for i in goodslist:
        if i in thing:
            data[0][i] += 1
        else:
            data[0][i] = 1
            thing.append(i)
    for s in range(len(goodslist)):
        if (timelist[s] == "03" or timelist[s] == "04" or timelist[s] == "05"):
            if goodslist[i] in spring:
                data[1][i] += 1
            else:
                data[1][i] = 1
                spring.append(goodslist[i])
        elif (timelist[s] == "06" or timelist[s] == "07" or timelist[s] == "08"):
            if goodslist[i] in summer:
                data[2][i] += 1
            else:
                data[2][i] = 1
                summer.append(goodslist[i])
        elif (timelist[s] == "09" or timelist[s] == "10" or timelist[s] == "11"):
            if goodslist[i] in autumn:
                data[3][i] += 1
            else:
                data[3][i] = 1
                autumn.append(goodslist[i])
        elif (timelist[s] == "12" or timelist[s] == "01" or timelist[s] == "02"):
            if goodslist[i] in winter:
                data[4][i] += 1
            else:
                data[4][i] = 1
                winter.append(goodslist[i])
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
    for key in dict[0]:
        cursor.execute("insert into goods_number (goods_id,namber) values(%d,%d)" % (key, dict[0][key]))
    for key in dict[1]:
        cursor.execute("insert into goods_number namber values %d" % (dict[1][key]))
    for key in dict[2]:
        cursor.execute("insert into goods_number namber values %d" % (dict[2][key]))
    for key in dict[3]:
        cursor.execute("insert into goods_number namber values %d" % (dict[3][key]))
    for key in dict[4]:
        cursor.execute("insert into goods_number namber values %d" % (dict[4][key]))
    db.commit()
    db.close()
    cursor.close()  # 关闭

if __name__ == '__main__':
    goodslist, timelist = reader.search()
    print(analysis_hot(goodslist,timelist))
