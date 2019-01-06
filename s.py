from flask_sqlalchemy import SQLAlchemy
import config
from flask import Flask,render_template

app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)

class Article(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.String(100),primary_key=True,autoincrement=False)#autoincrement自增长
    uname = db.Column(db.String(50),nullable=False)
    passwd = db.Column(db.String(50),nullable=False)

db.create_all()

@app.route("/")
def index():
    #增
    article1 = Article.query.filter(Article.uname == '稽水鎏年').first()
    if article1.uname == '稽水鎏年' and article1.passwd == 'jh1123456':
        return "ok"
    else:
        return "用户名或密码错误"

if __name__ == '__main__':
    app.run(debug=True)