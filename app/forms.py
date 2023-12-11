from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime


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


class UserLoginForm(FlaskForm):
    """
    Form for logging in user, for auth_views.py
    Notes:
        username: User ID for login (아이디)
        password: User Password for login (비밀번호)
    References:
        https://wikidocs.net/81058
    """
    username = StringField('사용자이름', validators=[DataRequired(), Length(min=1, max=30)])
    password = PasswordField('비밀번호', validators=[DataRequired()])


class DateRangeForm(FlaskForm):
    """
    Form for searching flights by date range, for airline_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    start_date = DateField('시작 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('종료 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('검색')


class SpecialInfoFrom(FlaskForm):
    """
    Form for shopping in special information, for purchase_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    specialInfoId = StringField('특이사항 번호', validators=[DataRequired()])


class DutyFreeFrom(FlaskForm):
    """
    Form for shopping in duty free shop, for purchase_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    itemId = StringField('상품번호', validators=[DataRequired()])
    quantity = StringField('수량', validators=[DataRequired()])
    submit = SubmitField('구매하기')

