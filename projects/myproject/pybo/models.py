# 위치 : C:/projects/myproject/pybo/models.py
# 내용 : 질문, 답변 모델 생성

from pybo import db

# 질문 모델
# id(기본키), subject(제목), content(내용), create_date(작성일)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)


# 답변 모델
# id(기본키), 질문id(질문 모델과 연결, 외부키), question(답변 모델에서 질문모델 참조하기 위해), content(내용), create_date(작성일)
# question의 backref 설정을 통해 질문이 삭제되면 해당 답변도 자동으로 삭제되게 설정
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
