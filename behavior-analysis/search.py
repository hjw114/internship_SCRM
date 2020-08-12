'''
本模块的作用是通过行为分析数据库得出具体用户行为关联性
author：胡觉文
'''
import reader
import apriori

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

def search(buy,results,rule):
    result = []
    for i in rule:
        for j in results:
            if i[0] == j:
                if i[1] not in buy:
                    result.append(i[1])
    result1 = [y for x in result for y in x]
    result2 = list(set(result1))
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
    dataSet = reader.data_handle(idlist, goodslist)
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    print(search(get(1, idlist, goodslist, actionlist),PowerSetsBinary(get(1, idlist, goodslist, actionlist)), rule))
    print(buy(1, idlist, goodslist, actionlist))