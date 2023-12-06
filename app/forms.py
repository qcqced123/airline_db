from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class UserCreateForm(FlaskForm):
    """ Form for creating new user
    Notes:
        username: User ID for login (아이디)
        password1: User Password for login (비밀번호)
        password2: for checking password1 (비밀번호 확인)
    References:
        https://wikidocs.net/81057
    """
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=3, max=25)])
    password1 = PasswordField(
        '비밀번호', validators=[DataRequired(), EqualTo('password2', '비밀번호가 일치하지 않습니다')]
    )
    password2 = PasswordField('비밀번호확인', validators=[DataRequired()])

