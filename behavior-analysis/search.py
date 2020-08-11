'''
本模块的作用是通过行为分析数据库得出具体用户行为关联性
author：胡觉文
'''
import reader
import pymysql

def get(id,idlist,goodslist,actionlist):#获取用户行为
    buy = []
    for s in range(len(idlist)):
        if idlist[s] == id:
            if actionlist[s] == 2:
                buy.append(goodslist[s])
    buy1 = list(set(buy))#去重
    return buy1

def PowerSetsBinary(buy):#求出用户行为子集
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

def sql_data():#取出行为数据库中用户行为
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

def search(buy,results, freqlist, conslist):#寻找对应行为
    result = []
    for i in range(len(freqlist)):
        for j in results:
            if freqlist[i] == j:
                if conslist[i] not in buy:#判断是否对应行为，是否和已有行为重复
                    result.append(conslist[i])
    result1 = [y for x in result for y in x]#一维展开
    result2 = list(set(result1))#去重
    return result2

def buy(id,idlist,goodslist,actionlist):#分析最大购买种类
    buy = []
    res = []
    result = {}
    for s in range(len(idlist)):#对应数据
        if idlist[s] == id:
            if actionlist[s] == 1:
                buy.append(goodslist[s])
    for s in buy:#判断成字典
        if s in res:
            result[s] += 1
        else:
            result[s] = 1
            res.append(s)
    return result

if __name__ == '__main__':
    idlist, goodslist, actionlist = reader.search()
    freqlist, conslist,_ = sql_data()
    print(search(get(1,idlist,goodslist,actionlist), PowerSetsBinary(get(1,idlist,goodslist,actionlist)), freqlist, conslist))
    print(buy(1,idlist,goodslist,actionlist))