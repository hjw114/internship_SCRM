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
@app.route("/homepage")
def homepage():
        # 跳转到网页
        return render_template("homepage.html")



if __name__ == '__main__':
        app.run()  # 启动服务器
