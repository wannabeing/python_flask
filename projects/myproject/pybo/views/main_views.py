from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')


@bp.route('/hello')
def hello_pybo():
    return 'This is main_views.py with HelloRouteFucntion'


@bp.route('/')
def index():
    # redirect : 입력받은 URL로 리다이렉트, url_for 함수는 라우트가 설정된 함수명으로 URL을 찾아줌.
    return redirect(url_for('question._list'))