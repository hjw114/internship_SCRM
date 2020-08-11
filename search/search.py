'''
本模块功能为根据用户输入的信息查找对应商品
author：胡觉文
'''
import pymysql

def search():#搜集商品信息
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')  # 数据库
    cursor = db.cursor()  # 游标
    sql1 = "SELECT goods_id FROM goods_information "
    cursor.execute(sql1)
    idlist = []
    allid = cursor.fetchall()  # 取出数据
    for s in allid:
        idlist.append(s[0])
    sql1 = "SELECT goods_name FROM goods_information "
    cursor.execute(sql1)
    namelist = []
    allname = cursor.fetchall()  # 取出数据
    for s in allname:
        namelist.append(s[0])
    db.commit()
    db.close()
    cursor.close()  # 关闭
    dict = {}
    for s in range(len(idlist)):#id和名字对应
        dict[idlist[s]] = namelist[s]
    return dict

def get(object,dict):#判断搜索关键字的id
    results = []
    for id,thing in dict.items():#遍历名字对应关键字
        if object in thing:
            results.append(id)
    if object == "":
        results = []
    return results

if __name__ == '__main__':
    th = input("请输入物品名字：")
    print(get(th,search()))