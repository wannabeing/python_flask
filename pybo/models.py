# 위치 : C:/projects/myproject/pybo/models.py
# 내용 : 질문, 답변 모델 생성
# DB 관련된 파일이므로, flask db migrate, upgrade가 필요함

from pybo import db


# 추천 모델
# 글 1개에 여러명이 추천, 1명이 여러글에 추천 - 다대다 관계
question_voter = db.Table(
    'question_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('question_id', db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), primary_key=True)
)

answer_voter = db.Table(
    'answer_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('answer_id', db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), primary_key=True)
)


# 질문 모델
# id(기본키), subject(제목), content(내용), create_date(작성일)
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))
    modify_date = db.Column(db.DateTime(), nullable=True) # 수정 필드 추가
    voter = db.relationship('User', secondary=question_voter, backref=db.backref('question_voter_set')) # 추천 필드 추가


# 답변 모델
# id(기본키), 질문id(질문 모델과 연결, 외부키), question(답변 모델에서 질문모델 참조하기 위해), content(내용), create_date(작성일)
# question의 backref 설정을 통해 질문이 삭제되면 해당 답변도 자동으로 삭제되게 설정
class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    modify_date = db.Column(db.DateTime(), nullable=True) # 수정 필드 추가
    voter = db.relationship('User', secondary=answer_voter, backref=db.backref('answer_voter_set'))


# 회원(User) 모델
# id : 기본키로써 자동으로 증가
# username, email에 unique=True 옵션은 '같은 값을 저장할 수 없다는 뜻', 이렇게 해야 username과 email이 중복되지 않는다.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


# 댓글(Comment) 모델
# 질문 또는 답변을 DB에서 삭제하면 연관된 댓글도 삭제될 수 있도록 ondelete='CASCADE' 설정
# id : 댓글 고유번호, user_id : 댓글 작성자(User와 관계), content(댓글 내용), question_id(Question과 관계), answer_id(Answer과 관계)
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime())
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'), nullable=True)
    question = db.relationship('Question', backref=db.backref('comment_set'))
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id', ondelete='CASCADE'), nullable=True)
    answer = db.relationship('Answer', backref=db.backref('comment_set'))