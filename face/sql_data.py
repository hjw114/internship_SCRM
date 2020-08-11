'''
本模块的功能为写入用户id，查找用户id
author：胡觉文
'''
import pymysql

def add(n):#增加数据
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')#数据库
    cursor = db.cursor()#游标
    cursor.execute("INSERT INTO user_id ({key}) VALUES ({value})".format(key="user_id",value=str(n)))
    db.commit()
    db.close()
    cursor.close()#关闭

def serach():#查找数据
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')
    cursor = db.cursor()
    sql1 = "SELECT user_id FROM user_id "
    cursor.execute(sql1)
    datalist = []
    alldata = cursor.fetchall()#取出数据
    for s in alldata:
        datalist.append(s[0])
    db.close()
    cursor.close()
    return datalist

if __name__ == '__main__':
    add(1)
    print(serach())
