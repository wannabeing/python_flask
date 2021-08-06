# 회원가입 뷰 (sign_view로 바꾸고 싶음)
import functools
from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

# /auth/라는 접두어로 시작하는 URL이 호출되면 auth_views.py 파일의 함수들이 호출할 수 있는 블루프린트 변수 추가
bp = Blueprint('auth', __name__, url_prefix='/auth')


# 회원가입을 수행할 라우트 함수
# POST = 회원가입 수행, GET = 회원가입 템플릿을 렌더링
@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data), # password는 hash 함수로 암호화저장
                        email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form)


# 로그인을 수행할 라우트 함수
# POST = 로그인 수행, GET = 로그인 템플릿 렌더링
@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data): # password는 hash 함수로 저장받고, hash 값으로 비교
            error = "비밀번호가 올바르지 않습니다."
        if error is None:  # 사용자도 존재하고 비밀번호도 맞으면 다음 라인 수행
            session.clear()
            session['user_id'] = user.id    # 플라스크 세션에 키와 키 값을 저장한다.
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


# 모든 라우트 함수보다 먼저 실행된다.
@bp.before_app_request
def load_logged_in_user():
    # 세션 변수에 user_id 값이 있으면 DB를 조회하여 g.user에 저장한다.
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)


#  로그아웃을 수행하는 라우트 함수
#  세션의 모든 값을 삭제하는 session.clear(), 따라서 g.user=None이 된다.
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view