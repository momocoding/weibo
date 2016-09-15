from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import Blueprint
from flask import abort
from flask import session


from models import User
from models import Weibo
from models import Comment


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字，第二个参数是套路
main = Blueprint('weibo', __name__)


def current_user():
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(uid)
        return u


@main.route('/<username>')
def index(username):
    cu = current_user()
    status = False
    if cu is not None:
        if cu.username == username:
            status = True
        current = cu.username
    else:
        current = '游客'

    if username == '游客':
        return redirect(url_for('user.login_view'))
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    else:
        weibos = Weibo.query.filter_by(user_id=username).order_by('created_time desc').all()

        # 把想要的数据先通过数据库取得，再把取得的数据通过属性的方式加到类实例中，很厉害
        for w in weibos:
            w.load_comments()
        return render_template('weibo_index.html', weibos=weibos, status=status, current=current)


# @main.route('/add', methods=['POST'])
# def add():
#     u = current_user()
#     if u is None:
#         return redirect(url_for('user.login_view'))
#     else:
#         form = request.form
#         w = Weibo(form)
#         w.user_id = u.username
#         if w.valid():
#             w.save()
#         else:
#             abort(400)
#         return redirect(url_for('weibo.index', username=u.username))


@main.route('/delete/<int:weibo_id>')
def delete(weibo_id):
    u = current_user()
    w = Weibo.query.get(weibo_id)
    w.delete()
    return redirect(url_for('weibo.index', username=u.username))


@main.route('/update/<int:weibo_id>', methods=['POST'])
def update(weibo_id):
    u = current_user()
    content = request.form.get('update', '')
    if len(content) == 0:
        abort(404)
    else:
        w = Weibo.query.get(weibo_id)
        w.content = content
        w.save()
        return redirect(url_for('weibo.index', username=u.username))


# @main.route('/comment/<int:weibo_id>', methods=['POST'])
# def comment(weibo_id):
#     u = current_user()
#     if u is None:
#         return redirect(url_for('user.login_view'))
#     else:
#         form = request.form
#         c = Comment(form)
#         c.user_id = u.username
#         c.weibo_id = weibo_id
#         if c.valid():
#             c.save()
#         else:
#             abort(400)
#         return c.json_string()
#         # w = Weibo.query.filter_by(id=weibo_id).first()
#         # return redirect(url_for('weibo.index', username=w.user_id))


@main.route('/')
def all():
    # 查找所有的 weibo 并返回
    status = False
    cu = current_user()
    if cu is not None:
        current = cu.username
    else:
        current = '游客'
    weibos = Weibo.query.order_by('created_time desc').all()
    for w in weibos:
        w.load_comments()
    return render_template('weibo_index.html', weibos=weibos, status=status, current=current)