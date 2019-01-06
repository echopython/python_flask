from flask import Flask,render_template,request,url_for,session,redirect,flash
from spider import content
from flask_sqlalchemy import SQLAlchemy
import config
from models import User,Question,Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_
from werkzeug.security import generate_password_hash,check_password_hash

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



@app.route('/')
def index():
    return render_template('index.html')

#注册提交url
@app.route('/registe/',methods=['GET','POST'])
def registe():
    if request.method == 'GET':
        return render_template('registe.html')
    else:
        username = request.form.get("username")
        pass_wd = request.form.get("passwd")
        pass_wd2 = request.form.get("passwd2")
        user = User.query.filter(User.uname == username).first()
        if user:
            return "该账号已被注册！请更换账号！"
        else:
            if pass_wd != pass_wd2:
                return "两次密码不相等，请核对！"
            else:
                user = User(uname=username,passwd=pass_wd)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
#登录提交url
@app.route("/login/",methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.uname == username).first()
        if user and user.check_password(password):
            session['name'] = user.uname
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return "账号或密码错误！"
#个人信息
@app.route("/info")
def info():
    return render_template("info.html")

#我的文章页
@app.route("/my_article")
@login_required
def my_article():
    user_id = User.query.filter(User.uname == session['name']).first()
    article_id = Question.query.filter(Question.author_id == user_id.id).all()
    context = {
        'my_articles': article_id
    }
    return render_template('my_article.html', **context)

#删除文章
@app.route("/delete_article",methods=["GET","POST"])
def delete_article():
    if request.method =="GET":
        return render_template("my_article.html")
    else:
        q_id = request.form.get("q_id")
        #ans = Answer.query.filter(Answer.question_id == q_id).all()
        ans_q = Question.query.filter(Question.id == q_id).first()
        db.session.delete(ans_q)
        db.session.commit()
        return redirect(url_for("my_article"))
#注销
@app.route("/clear")
def clear():
    session.clear()
    return render_template("login.html")

#修改密码
@app.route("/upPassWord/",methods=['GET','POST'])
def upPassWord():

    if request.method == 'GET':
        return render_template('info.html')
    else:
        new_password1 = request.form.get('new_password1')

        new_password2 = request.form.get('new_password2')
        user = User.query.filter(User.uname == session['name']).first()
        if new_password1 != new_password2:
            return "两次密码不相等，请核对后输入！"
        else:
            user.passwd = generate_password_hash(new_password1)
            db.session.commit()
            session.clear()
        return redirect(url_for('login'))
#修改用户名
@app.route("/upUserName/",methods=['GET','POST'])
def upUserName():
    if request.method == 'GET':
        return render_template("info.html")
    else:
        new_username = request.form.get("new_username")
        user = User.query.filter(User.uname == session['name']).first()
        user.uname = str(new_username)
        db.session.commit()
        session.clear()
    return redirect(url_for('login'))

#发布问答页
@app.route("/question/",methods=['GET','POST'])
@login_required
def question():

    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id = session.get('name')
        user = User.query.filter(User.uname == user_id).first()
        question.author = user
        db.session.add(question)

        db.session.commit()
        return redirect(url_for('article'))
#热门页
@app.route("/article/")
def article():
    context = {
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('article.html',**context)

#详情页
@app.route("/detail/<question_id>/")
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()

    return render_template('detail.html',question = question_model)


@app.route("/add_answer/",methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['name']
    user = User.query.filter(User.uname == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/search/')
def search():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),
                              Question.content.contains(q))).order_by('-create_time')
    return render_template('article.html',questions=questions)

@app.route('/follow/<uname>')
@login_required
def follow(uname):
    user = User.query.filter_by(uname=uname).first()
    if user is None:
        flash('用户不存在')
        return redirect(url_for('article'))
    if User.is_following(user,user):
        flash('您已关注该用户')
        return redirect(url_for('article.user',uname=uname))
    User.follow(user,user)
    flash('已关注')
    return redirect(url_for('article.user',uname=uname))


if __name__ == '__main__':
    app.run(debug=True)
