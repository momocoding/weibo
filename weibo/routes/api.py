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


@main.route('/weibo/update/<int:weibo_id>', methods=['POST'])
def update(weibo_id):
    content = request.form.get('content', '')
    print('content', content)
    w = Weibo.query.get(weibo_id)
    w.content = content
    if w.valid():
        w.save()
        r = w.success_response()
        r['message'] = '更新成功'
    else:
        r = w.error_response()
    return json.dumps(r, ensure_ascii=False)


@main.route('/comment/add', methods=['POST'])
def comment_add():
    u = current_user()
    print('1111')
    if u is None:
        r = dict(
            success=302,
            message='请登录之后评论',
        )
        return json.dumps(r, ensure_ascii=False)
    else:
        form = request.form
        c = Comment(form)
        c.user_id = u.username
        if c.valid():
            c.save()
            r = c.success_response()
        else:
            r = c.error_response()
        print('33333')
        return json.dumps(r, ensure_ascii=False)


@main.route('/weibo/add', methods=['POST'])
def add():
    u = current_user()
    form = request.form
    w = Weibo(form)
    w.user_id = u.username
    if w.valid():
        w.save()
        r = w.success_response()
    else:
        r = w.error_response()
    return json.dumps(r, ensure_ascii=False)


@main.route('/weibo/delete/<int:weibo_id>')
def delete(weibo_id):
    w = Weibo.query.get(weibo_id)
    w.delete()
    r = dict(
        success=True,
        message='删除成功',
    )
    return json.dumps(r, ensure_ascii=False)