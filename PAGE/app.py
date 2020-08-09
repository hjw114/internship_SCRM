from flask import Flask, render_template, request
import pymysql
import get
import judge_people
import sql_data
import LBPHFaceRecognizer
import master
import sqlite_add

app = Flask(__name__)
global userid
userid = 1
'''
@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
    from flask import Flask, render_template, request

    app = Flask(__name__)
    '''
@app.route('/test')
def hello_world():
        return '123'


@app.route('/register')
def register():


        return render_template("register.html")


    # 显示注册界面
@app.route("/")
def homepage():
        u = hot_goods()
        u2 = season_goods()
        return render_template("homepage.html", u=u, u2=u2)

@app.route("/douser")
def douser():
    usersid = master.master()
    if usersid >= 0:
        userid = usersid
    else:
        userid = master.master()
    print(userid)
    u = hot_goods()
    u1 = like()
    u2 = season_goods()
    return render_template("homepage_people.html", u=u, u1=u1, u2=u2)

@app.route("/homepage_people")
def homepage_people():
    u = hot_goods()
    u1 = like()
    u2 = season_goods()
    return render_template("homepage_people.html", u=u, u1=u1, u2=u2)

def hot_goods():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql = "SELECT `goods_id`,`goods_name`,`goods_price`  FROM goods_information  " \
          "WHERE `goods_id` like '%001'OR`goods_id` like '%101' ORDER BY `goods_sales`DESC "
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return u

def season_goods():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql3 = " SELECT `goods_id`,`goods_name`,`goods_price` FROM goods_information " \
           "WHERE `goods_id` like '%001'OR`goods_id` like '%101' AND LEFT(goods_id,6) " \
           "IN (SELECT t.goods_id FROM (SELECT * FROM goods_number  ORDER BY `summer` DESC limit 0,100 )as t )"
    cur.execute(sql3)
    u3 = cur.fetchall()
    conn.close()
    return u3

def season_goods_id():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    temp = "SELECT `goods_id` FROM goods_number ORDER BY `summer` DESC"
    cur.execute(temp)
    season_id = cur.fetchall()
    conn.close()
    return season_id


def like():
    u2 = 40
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql1 ="  select `goods_id`,`goods_name`,`goods_price` from goods_information WHERE  `goods_id`  like '40%' AND " \
          "`goods_id` like '%001'"
    cur.execute(sql1)
    u1 = cur.fetchall()
    conn.close()
    return u1

def people_like():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql2 = "SELECT SUBSTR(goods_id, 1,2) FROM user_behavior WHERE `users_id`=%s "% (userid)
    cur.execute(sql2)
    u1 = cur.fetchall()
    conn.close()
    temp = 0
    for u2 in u1:
        if u1.count(u2) > temp:
            max_str = u2
            temp = u1.count(u2)
    return max_str



@app.route("/Personal_homepage")
def Personal_homepage():
     u = person_information()
     times = person_shopping()
     goods_information = find_goods()
     return render_template("Personal_homepage.html", u=u, times=times, goods_information=goods_information)

def person_information():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql = "SELECT `user_name`,`user_number`,`user_address`  FROM user_id WHERE `user_id`=%s" % (userid)
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return u

def person_shopping():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql = "SELECT `times` FROM user_behavior WHERE `users_id`=%s" % (userid)
    cur.execute(sql)
    times = cur.fetchall()
    conn.close()
    return times

def find_goods():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql = "SELECT `goods_name`,`goods_price` FROM goods_information WHERE `goods_id` " \
          "IN (SELECT `goods_id` FROM user_behavior WHERE `users_id`=%s AND actions = 1)" % (userid)
    cur.execute(sql)
    goods_information = cur.fetchall()
    conn.close()
    return goods_information

@app.route("/payment")
def payment():
        return render_template("payment.html")

@app.route("/check")
def check():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730',
                           port=3306, db='demo')
    cur = conn.cursor()
    sql2 = "SELECT goods_id,goods_name,goods_price  FROM goods_information WHERE goods_id " \
           "In(SELECT goods_id  FROM user_behavior WHERE `users_id`=%s AND actions = 2) " % (userid)
    cur.execute(sql2)
    u2 = cur.fetchall()
    conn.close()
    return render_template("check.html", u=u2)

@app.route("/shoppinglist")
def shoppinglist():
    return render_template("Shoppinglist.html")

@app.route("/shoppinglist2")
def shoppinglist2():
    return render_template("Shoppinglist2.html")

@app.route("/shoppinglist3")
def shoppinglist3():
    return render_template("Shoppinglist3.html")






@app.route("/ajax",methods=['get','post'])
def get_ajax():
        # 获取前端发送过来的内容

        user_id = userid
        action = request.values.get("action")
        goods_id = request.values.get("goods_id")
        time = request.values.get("time")

        sqlite_add.Add(user_id,action,goods_id,time)

        return "successful"

@app.route("/Shopping_Cart")
def shopping_cart():
    u1 = like()
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',user='root',password='Wxs20200730',port=3306,db='demo')
    cur = conn.cursor()
    sql2 = "SELECT goods_id,goods_name,goods_price  FROM goods_information WHERE goods_id " \
           "In(SELECT goods_id  FROM user_behavior WHERE `users_id`=%s AND actions = 2) "% (userid)
    cur.execute(sql2)
    u2 = cur.fetchall()
    conn.close()
    return render_template("ShoppingCart.html", u=u2, u1=u1)


@app.route("/Payment")
def Payment():
        return render_template("Payment.html")

if __name__ == '__main__':
        app.run()  # 启动服务器
