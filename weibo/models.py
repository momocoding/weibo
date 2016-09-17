from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import time
import json

# 以下都是套路
app = Flask(__name__)
app.secret_key = 'secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 指定数据库的路径
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

db = SQLAlchemy(app)


class ModelHelper(object):
    def __repr__(self):
        """
        __repr__ 是一个魔法方法
        简单来说, 它的作用是得到类的 字符串表达 形式
        比如 print(u) 实际上是 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format_time(self, t):
        format = '%Y/%m/%d %H:%M:%S'
        value = time.localtime(int(time.time()))
        dt = time.strftime(format, value)
        return dt


# 定义一个 Model，继承自 db.Model
class Todo(db.Model, ModelHelper):
    __tablename__ = 'todos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.task = form.get('task', '')
        self.created_time = int(time.time())

    def valid(self):
        return len(self.task) > 0


class User(db.Model, ModelHelper):
    __tablename__ = 'users'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    created_time = db.Column(db.Integer, default=0)

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = int(time.time())

    def valid(self):
        return len(self.username) >= 2 and len(self.password) > 2

    def validate_login(self, u):
        return u.username == self.username and u.password == self.password

    def change_password(self, password):
        if len(password) > 2:
            self.password = password
            self.save()
            return True
        else:
            return False


class Weibo(db.Model, ModelHelper):
    __tablename__ = 'Weibos'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.String())
    # 定义关系
    user_id = db.Column(db.String())
    comments = []

    def __init__(self, form):
        self.content = form.get('content', '')
        self.created_time = self.format_time(int(time.time()))

    def valid(self):
        if len(self.content) != 0 and len(self.content) <= 140:
            return True
        return False

    def load_comments(self):
        self.comments = Comment.query.filter_by(weibo_id=self.id).all()

    def to_dict(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
            'comments': self.load_comments()
        }
        return d

    def valid_len(self):
        if len(self.content) == 0:
            message = '微博不能为空'
        else:
            message = '微博不能超过140个字'
        return message


class Comment(db.Model, ModelHelper):
    __tablename__ = 'Comments'
    # 下面是字段定义
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String())
    created_time = db.Column(db.String())
    # 定义关系
    user_id = db.Column(db.String())
    weibo_id = db.Column(db.Integer)

    def __init__(self, form):
        self.content = form.get('content', '')
        self.weibo_id = form.get('weibo_id', '')
        self.created_time = self.format_time(int(time.time()))

    def valid(self):
        if len(self.content) != 0 and len(self.content) <= 40:
            return True
        return False

    def to_dict(self):
        d = {
            'id': self.id,
            'content': self.content,
            'created_time': self.created_time,
            'user_id': self.user_id,
            'weibo_id': self.weibo_id,
        }
        return d

    def valid_len(self):
        if len(self.content) == 0:
            message = '评论不能为空'
        else:
            message = '评论不能超过40字'
        return message


if __name__ == '__main__':
    # 先 drop_all 删除所有数据库中的表
    # 再 create_all 创建所有的表
    db.drop_all()
    db.create_all()
    print('rebuild database')
