from flask import Flask, render_template, request
import pymysql
import apriori
import master
import search
import reader
import datetime


app = Flask(__name__)
# 初始化全局变量
global userid,user_num
userid = 2
user_num = "0"

# 用户访问序号
def getnumber():
    db = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', password='Wxs20200730', port=3306,
                         db='demo')
    cursor = db.cursor()
    sql1 = "SELECT users_number FROM user_number "
    cursor.execute(sql1)
    datalist = []
    alldata = cursor.fetchall()  # 取出数据
    for s in alldata:
        datalist.append(s[0])
    db.close()
    cursor.close()
    user_num = datalist[-1]
    return user_num

# 登录页面
@app.route('/register')
def register():
        user_num = str(getnumber() + 1)
        return render_template("register.html", user_num = user_num)

# 识别页面
@app.route("/douser")
def douser():
    path = "D:/USER/DOWN/2.mp4"
    usersid = master.master(path)
    if usersid >= 0:
        userid = usersid
    else:
        userid = master.master(path)
    print(userid)
    u = hot_goods()
    u1 = like()
    lenu1 = len(u1)
    u22 = []
    temp = season_goods()
    for i in temp:
        u22.append(i[0])
    u2 = u22[::2]
    return render_template("homepage_people.html", u=u, u1=u1, u2=u2, lenu1=lenu1)




    # 显示主界面

# 首页
@app.route("/")
def homepage():
        u = hot_goods()
        u22 = []
        temp = season_goods()
        for i in temp:
            u22.append(i[0])
        u2 = u22[::2]
        return render_template("homepage.html", u=u, u2=u2)

@app.route("/homepage_people")
def homepage_people():
    u = hot_goods()
    u1 = like()
    lenu1 = len(u1)
    u22 = []
    temp = season_goods()
    for i in temp:
        u22.append(i[0])
    u2 = u22[::2]
    return render_template("homepage_people.html", u=u, u1=u1, u2=u2, lenu1=lenu1)

# 导购员页面
@app.route("/guide")
def guide():
        guestid = None
        u = hot_goods()
        u22 = []
        temp = season_goods()
        for i in temp:
            u22.append(i[0])
        u2 = u22[::2]
        if(guestid):
            u3 = person_information(guestid)
            goods_information = find_goods(guestid)
            return render_template("guide.html", u=u, u2=u2, u3=u3, goods_information=goods_information,guestid=guestid)
        else:
            return render_template("guide.html", u=u, u2=u2, guestid=guestid)

@app.route("/findID",methods=['POST'])
def findguest():
    u = hot_goods()
    u22 = []
    temp = season_goods()
    for i in temp:
        u22.append(i[0])
    u2 = u22[::2]
    id = request.form.get('guestid')
    guestid = str(id)
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cls = conn.cursor()
    # 前端传递的数据，进行到数据库中进行验证
    cls.execute("select `user_id` from user_id where user_id=%s ", [guestid])
    result = cls.fetchone()
    conn.close()
    if (guestid):
        if (result):
            u3 = None
        u3 = person_information(guestid)
        goods_information = find_goods(guestid)
        guestgoods = guestlike(guestid)
        return render_template("guide.html", u=u, u2=u2, u3=u3, goods_information=goods_information, guestid=guestid,guestgoods=guestgoods)
    else:
        return render_template("guide.html", u=u, u2=u2, guestid=guestid)

def guestlike(guestid):
    guestid = int(guestid)
    idlist, goodslist, actionlist = reader.search()
    dataSet = reader.data_handle(idlist, goodslist)
    L, supportData = apriori.apriori(dataSet, minSupport=0.2)
    rule = apriori.gen_rule(L, supportData, minConf=0.7)
    glike = search.search(search.PowerSetsBinary(search.get(guestid, idlist, goodslist, actionlist)), rule)
    print(glike)
    guestlike = []
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    for i in glike:
        j = str(i) + '%'
        sql3 = " SELECT `goods_id`,`goods_name`,`goods_price` FROM goods_information " \
               "WHERE  `goods_id` like '%s'" % (j)
        cur.execute(sql3)
        u3 = cur.fetchone()
        guestlike.append(u3)
    conn.close()
    return guestlike

# 搜索页面
@app.route("/search",methods=['POST'])
def searchgoods():
    goods = request.form.get('search')
    goods = str(goods)
    goods_name = '%' +goods+'%'
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                            user='root',
                            password='Wxs20200730',
                            port=3306,
                            db='demo')
    cls = conn.cursor()
     # 前端传递的数据，进行到数据库中进行验证
    cls.execute("select `goods_id`,`goods_name`,`goods_price` from goods_information where `goods_name` LIKE '%s' "% (goods_name))
    goodslist = cls.fetchall()
    conn.close()
    return render_template("Search.html",goodslist=goodslist)

@app.route("/hotgoods")
def hotgoods():
    u = hot_goods()
    return render_template("hot.html", u=u)

@app.route("/seasonhot")
def seasonhot():
    u22 = []
    temp = season_goods()
    for i in temp:
        u22.append(i[0])
    u2 = u22[::2]
    return render_template("seasonhot.html",  u2=u2)


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
    sid = season_goods_id()
    list = []
    n = '%' + '001'
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    for i in sid:
        j = str(i[0]) + '%'
        sql3 = " SELECT `goods_id`,`goods_name`,`goods_price` FROM goods_information " \
           "WHERE  `goods_id` like '%s'AND `goods_id` like '%s'" %(j,n)
        cur.execute(sql3)
        u3 = cur.fetchall()
        if(u3):
            list.append(u3)
    conn.close()
    return list

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
    n = people_like()
    u3 = '%' + '001'
    u2 = n[0] +'%'
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql1 ="select `goods_id`,`goods_name`,`goods_price` from goods_information " \
          "WHERE  `goods_id` like '%s'  AND  `goods_id` like '%s'" % (u3, u2)
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
    sql2 = "SELECT SUBSTR(goods_id, 1,2) FROM user_behavior WHERE `users_id`='2'"
    cur.execute(sql2)
    u1 = cur.fetchall()
    conn.close()
    temp = 0
    max_str = '0'
    for u2 in u1:
        if u1.count(u2) > temp:
            max_str = u2
            temp = u1.count(u2)
    return max_str

# 个人首页
@app.route("/Personal_homepage")
def Personal_homepage():
     u = person_information(userid)
     goods_information = find_goods(userid)
     return render_template("Personal_homepage.html", u=u,  goods_information=goods_information)

def person_information(id):
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql = "SELECT `user_name`,`user_number`,`user_address`  FROM users_information WHERE `user_id`=%s" % (id)
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return u

def find_goods(id):
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',
                           user='root',
                           password='Wxs20200730',
                           port=3306,
                           db='demo')
    cur = conn.cursor()
    sql ="SELECT * FROM goods_information LEFT JOIN user_behavior " \
         "ON goods_information.goods_id = user_behavior.goods_id WHERE `users_id`=%s AND (`actions` = 1)" \
         "UNION SELECT * FROM goods_information " \
         "RIGHT JOIN user_behavior " \
         "ON goods_information.goods_id = user_behavior.goods_id WHERE `users_id`=%s AND (`actions` = 1)" \
         "ORDER BY `times` desc"% (id, id)
    cur.execute(sql)
    goods_information = cur.fetchall()
    conn.close()
    return goods_information

# 购物车页面
@app.route("/Shopping_Cart")
def shopping_cart():
    guestgoods = guestlike(userid)
    return render_template("ShoppingCart.html", u=sqlite_search_shoppingcart(), guestgoods=guestgoods)

def sqlite_search_shoppingcart():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',user='root',password='Wxs20200730',port=3306,db='demo')
    cur = conn.cursor()
    sql2 = "SELECT goods_id,goods_name,goods_price  FROM goods_information WHERE goods_id " \
           "In(SELECT goods_id  FROM user_behavior WHERE `users_id`=%s AND actions = 2) "% (userid)
    cur.execute(sql2)
    u2 = cur.fetchall()
    conn.close()
    print(u2)
    print("查询数据成功")
    return(u2)

@app.route("/ajax_delete_shoppingcart",methods=['get','post'])
def ajax_delete_shoppingcart():
        # 获取前端发送过来的内容
        user_id = request.values.get("user_id")
        goods_id = request.values.get("goods_id")
        sqlite_delete_shoppingcart(user_id,goods_id)
        return "successful"
def sqlite_delete_shoppingcart(user_id,goods_id):
    conn = pymysql.connect (host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', port=3306,password='Wxs20200730',db='demo')
    print("已成功连接")
    print(conn)
    try:
        cursor=conn.cursor()
        # SQL 查询语句
        sql = "DELETE FROM user_behavior WHERE users_id=%s AND goods_id=%s AND actions='2'"% (user_id,goods_id)
        cursor.execute(sql)
        conn.commit()
        print ('删除数据成功')
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
        print('删除数据失败')
    finally:
	    # 关闭数据库
	    conn.close()

# 结算确认页面
@app.route("/check")
def check():
    return render_template("check.html")

@app.route("/ajax_check",methods=['get','post'])

def ajax_check():
        # 获取前端发送过来的内容
        consignee = request.values.get("consignee")
        contact = request.values.get("contact")
        address = request.values.get("address")

        num0 = request.values.get("num0");num1 = request.values.get("num1");num2 = request.values.get("num2");num3 = request.values.get("num3");num4 = request.values.get("num4")
        num5 = request.values.get("num5");num6 = request.values.get("num6");num7 = request.values.get("num7");num8 = request.values.get("num8");num9 = request.values.get("num9")
        num=[]
        num.append(num0);num.append(num1);num.append(num2);num.append(num3);num.append(num4)
        num.append(num5);num.append(num6);num.append(num7);num.append(num8);num.append(num9)

        goods_id=check_sqlite_search_userwanttobuy()
        check_sqlite_deleteandadd_order(userid,goods_id,num)
        if (address!=''and contact!=''and consignee!=''):
            check_sqlite_addanddelete_information(userid,consignee,contact,address)
        return "successful"

def check_sqlite_search_userwanttobuy():
    conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn',user='root',password='Wxs20200730',port=3306,db='demo')
    cur = conn.cursor()
    sql2 = "SELECT goods_id  FROM goods_information WHERE goods_id " \
           "In(SELECT goods_id  FROM user_behavior WHERE `users_id`=%s AND actions = 2) "% (userid)
    cur.execute(sql2)
    u2 = cur.fetchall()
    conn.close()
    print("查询数据成功")
    return(u2)

def check_sqlite_addanddelete_information(id1,id2,id3,id4):
    import pymysql
    conn = pymysql.connect (host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', port=3306,password='Wxs20200730',db='demo',charset="utf8")
    cursor=conn.cursor()
    try:
        sql = "DELETE FROM users_information WHERE user_id='%s'"% (id1)
        cursor.execute(sql)
        conn.commit()
        print("删除数据成功")
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
        print('删除数据失败')
    finally:
           # SQL 插入语句
            SQL = "insert into users_information (user_id,user_name,user_number,user_address) values('%s','%s','%s','%s')"%(id1,id2,id3,id4);
            cursor.execute(SQL)
            conn.commit()
            print ('插入数据成功')

def check_sqlite_deleteandadd_order(user_id, goodsid, nums):
            import pymysql
            conn = pymysql.connect(host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', port=3306,
                                   password='Wxs20200730', db='demo', charset="utf8")
            print("已成功连接")
            print(conn)
            cursor = conn.cursor()
            # 将从数据库里select得到的元组goods_id转化成数组
            goods_id = []
            for i in goodsid:
                goods_id.append(i[0])
            # 将有空值的字符串数组num转为数组
            a = 0;
            num_array = []
            while nums[a] != '':
                num_array.append(nums[a])
                a += 1
            for good_id, num in zip(goods_id, num_array):
                # 插入语句
                sql2 = "insert into user_behavior (users_id,actions,goods_id,times) values(%s,%s,%s,'%s')" % (
                user_id, 1, good_id, datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
                b = 0
                while (b < int(num)):
                    cursor.execute(sql2)
                    conn.commit()
                    print('插入数据成功')
                    b = b + 1;
                # SQL 删除
                sql = "DELETE FROM user_behavior WHERE users_id=%s  AND actions='2'AND goods_id=%s" % (user_id, good_id)
                cursor.execute(sql)
                conn.commit()
                print('删除数据成功')
            # 关闭数据库
            conn.close()


# 商品页面 对应商品序号
@app.route("/10201101")
def shoppinglist1():
    return render_template("10201101.html")

@app.route("/20100001")
def shoppinglist2():
    return render_template("20100001.html")

@app.route("/20500001")
def shoppinglist3():
    return render_template("20500001.html")

@app.route("/20100001")
def shoppinglist4():
    return render_template("20100001.html")

@app.route("/30300001")
def shoppinglist5():
    return render_template("30300001.html")

@app.route("/30300002")
def shoppinglist6():
    return render_template("30300002.html")

@app.route("/40000001")
def shoppinglist7():
    return render_template("40000001.html")

@app.route("/40100001")
def shoppinglist8():
    return render_template("40100001.html")

@app.route("/50000001")
def shoppinglist9():
    return render_template("50000001.html")

@app.route("/50200001")
def shoppinglist10():
    return render_template("50200001.html")

@app.route("/60100001")
def shoppinglist11():
    return render_template("60100001.html")

@app.route("/60200001")
def shoppinglist12():
    return render_template("60200001.html")

@app.route("/70000001")
def shoppinglist13():
    return render_template("70000001.html")

@app.route("/70100101")
def shoppinglist14():
    return render_template("70100101.html")

@app.route("/70200001")
def shoppinglist15():
    return render_template("70100101.html")

@app.route("/70300001")
def shoppinglist16():
    return render_template("70300001.html")

@app.route("/30200001")
def shoppinglist17():
    return render_template("30200001.html")


@app.route("/ajax",methods=['get','post'])
def get_ajax_shoppingcart():
        # 获取前端发送过来的内容
        goods_id = request.values.get("goods_id")
        Add(userid,goods_id)
        return "successful"

def Add(id1,id2):
    import datetime
    import pymysql
    conn = pymysql.connect (host='wxs.chinaeast.cloudapp.chinacloudapi.cn', user='root', port=3306,password='Wxs20200730',db='demo')
    print("已成功连接")
    print(conn)
    try:
        cursor=conn.cursor()
        # SQL 插入语句
        SQL = "insert into user_behavior (users_id,actions,goods_id,times) values(%s,%s,%s,'%s');"%(id1,2,id2,datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
        cursor.execute(SQL)
        conn.commit()
        print ('插入数据成功')
    except Exception as e:
        print(e)
        # 回滚
        conn.rollback()
        print('插入数据失败')
    finally:
       # 关闭数据库
       conn.close()

# 结算扫脸页面
@app.route("/Payment")
def Payment():
        return render_template("Payment.html")


if __name__ == '__main__':
        app.run()  # 启动服务器
