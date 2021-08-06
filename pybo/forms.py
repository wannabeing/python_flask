from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class QuestionForm(FlaskForm):
    subject = StringField('제목', validators=[DataRequired('제목을 입력해주세요.')])
    content = TextAreaField('내용', validators=[DataRequired('내용을 입력해주세요.')])


class AnswerForm(FlaskForm):
        content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])


# username은 필수항목이면서, 길이를 제한해야하므로 validators 옵션에 필수항목으로 DataRequired, 길이조건을 추가
# password1,2 값은 일치해야하므로 validators 옵션에 EqualTo 검증을 추가
# email에는 필수항목과 더불어 이메일형식인지 검사해주는 Email()을 추가, email-validator를 설치해야 함
# password1, 2는 이후 템플릿 코드를 자동으로 생성할 때 <input type="password">가 된다.
# email은 이후 템플릿 코드를 자동으로 생성할 때 <input type="email">이 된다.

class UserCreateForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[
        DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])
    email = EmailField('이메일', validators=[DataRequired(), Email()])


# 로그인 폼 구현
class UserLoginForm(FlaskForm):
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


# 댓글 폼 구현
class CommentForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired()])