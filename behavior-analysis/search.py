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

def max(rule):
    max = 0
    for i in rule:
        if max < len(i[0]):
            max = len(i[0])
    return max

def PowerSetsBinary(buy,max):
    results = []
    N = len(buy)
    for i in range(2 ** N):  # 子集个数，每循环一次一个子集
        combo = []
        for j in range(N):  # 用来判断二进制下标为j的位置数是否为1
            if (i >> j) % 2:
                if buy[j] != []:
                    combo.append(buy[j])
        if len(combo) <= max:
            results.append(combo)
    del(results[0])
    return results

def search(results,rule):
    result = []
    for i in rule:
        for j in results:
            if i[0] == j:
                result.append(i[1])
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
    dataSet = reader.data_handle(idlist, goodslist)
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    print(search(PowerSetsBinary(get(1,idlist,goodslist,actionlist),max(rule)),rule))
    print(buy(1,idlist,goodslist,actionlist))