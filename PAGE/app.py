from flask import Flask, render_template
app = Flask(__name__)

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
        # 跳转到网页
        return render_template("homepage.html")

@app.route("/homepage_people")
def homepage_people():
        return render_template("homepage_people.html")

@app.route("/Personal_homepage")
def Personal_homepage():
        return render_template("Personal_homepage.html")

@app.route("/payment")
def payment():
        return render_template("payment.html")

@app.route("/check")
def check():
        return render_template("check.html")

@app.route("/shoppinglist")
def Pumpkin_pie():
        return render_template("Shoppinglist.html")

@app.route("/Shopping_Cart")
def Shopping_Cart():
        return render_template("ShoppingCart.html")

@app.route("/Payment")
def Payment():
        return render_template("Payment.html")

if __name__ == '__main__':
        app.run()  # 启动服务器
