import reader
import apriori
import pymysql

def get(id,idlist,goodslist,actionlist):
    buy = []
    for s in range(len(idlist)):
        if idlist[s] == id:
            if actionlist[s] == 2:
                buy.append(goodslist[s])
    buy1 = list(set(buy))
    return buy1

def PowerSetsBinary(buy):
    results = []
    N = len(buy)
    for i in range(2 ** N):  # 子集个数，每循环一次一个子集
        combo = []
        for j in range(N):  # 用来判断二进制下标为j的位置数是否为1
            if (i >> j) % 2:
                if buy[j] != []:
                    combo.append(buy[j])
    del(results[0])
    return results

def sql_data():
    sql_data = []
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql1 = "SELECT freqSet_conseq FROM behavior_analysis_aprior "
    cursor.execute(sql1)
    freqlist = []
    allfreq = cursor.fetchall()  # 取出数据
    for s in allfreq:
        freqlist.append(s[0])
    sql2 = "SELECT conseq FROM behavior_analysis_aprior "
    cursor.execute(sql2)
    conslist = []
    allcons = cursor.fetchall()  # 取出数据
    for s in allcons:
        conslist.append(s[0])
    sql3 = "SELECT conf FROM behavior_analysis_aprior "
    cursor.execute(sql3)
    conflist = []
    allconf = cursor.fetchall()  # 取出数据
    for s in allconf:
        conflist.append(s[0])
    db.commit()
    db.close()
    cursor.close()  # 关闭
    return freqlist, conslist, conflist

def search(results, freqlist, conslist):
    result = []
    for i in range(len(freqlist)):
        for j in results:
            if freqlist[i] == j:
                result.append(conslist[i])
    result1 = [y for x in result for y in x]
    result2 = list(set(result1))
    return result2

def buy(id,idlist,goodslist,actionlist):
    buy = []
    res = []
    result = {}
    for s in range(len(idlist)):
        if idlist[s] == id:
            if actionlist[s] == 1:
                buy.append(goodslist[s])
    for s in buy:
        if s in res:
            result[s] += 1
        else:
            result[s] = 1
            res.append(s)
    return result

def save_sql(result,id):
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql = "update user_id set want_to_buy = %s where id = %s"
    cursor.execute(sql,[str(result),str(id)])
    db.commit()
    db.close()
    cursor.close()  # 关闭

if __name__ == '__main__':
    idlist, goodslist, actionlist = reader.search()
    freqlist, conslist,_ = sql_data()
    print(search(PowerSetsBinary(get(1,idlist,goodslist,actionlist)), freqlist, conslist))
    print(buy(1,idlist,goodslist,actionlist))