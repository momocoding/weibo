from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import session
import json


from models import User
from models import Weibo
from models import Comment


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('api', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


def response(success, data=None, message=''):
    r = dict(
        success=success,
        data=data,
        message=message,
    )
    return json.dumps(r, ensure_ascii=False)


@main.route('/weibo/update/<int:weibo_id>', methods=['POST'])
def weibo_update(weibo_id):
    content = request.form.get('content', '')
    w = Weibo.query.get(weibo_id)
    w.content = content
    if w.valid():
        w.save()
        r = response(True, data=w.to_dict(), message='更新成功')
    else:
        message = w.valid_len()
        r = response(False, message=message)
    return r


@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    if u is None:
        r = response(302, message='请登录之后评论')
    else:
        form = request.form
        c = Comment(form)
        c.user_id = u.username
        if c.valid():
            c.save()
            r = response(True, data=c.to_dict(), message='评论成功')
        else:
            message = c.valid_len()
            r = response(False, message=message)
    return r


@main.route('/weibo/add', methods=['POST'])
def weibo_add():
    u = current_user()
    form = request.form
    w = Weibo(form)
    w.user_id = u.username
    if w.valid():
        w.save()
        r = response(True, data=w.to_dict(), message='发布成功')
    else:
        message = w.valid_len()
        r = response(False, message=message)
    return r


@main.route('/weibo/delete/<int:weibo_id>')
def weibo_delete(weibo_id):
    w = Weibo.query.get(weibo_id)
    w.delete()
    r = response(True, message='删除成功')
    return r
