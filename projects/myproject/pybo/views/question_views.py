from flask import Blueprint, render_template

from pybo.models import Question

bp = Blueprint('question', __name__, url_prefix='/question')


@bp.route('/list/')
def _list():
    question_list = Question.query.order_by(Question.create_date.desc()) #작성일 기준 역순으로 정렬
    return render_template('question/question_list.html', question_list=question_list)


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id) #question_id를 받았을 때 없는 id이면 404응답코드를 출력한다.
    return render_template('question/question_detail.html', question=question)