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


class StaffLoginForm(FlaskForm):
    """
    Form for logging in staff, for auth_views.py
    Notes:
        staff_name: staff ID for login (아이디)
        password: User Password for login (비밀번호)
    References:
        https://wikidocs.net/81058
    """
    staffID = StringField('임직원ID', validators=[DataRequired(), Length(min=1, max=30)])
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


class AddFlightDateRangeForm(FlaskForm):
    """
    Form for Add new Flight Schedule flights by date range, for staff_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    start_date = DateField('시작 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('종료 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    aircraftId = StringField('항공기 번호', validators=[DataRequired()])
    flightNumber = StringField('항공편 스케줄 번호', validators=[DataRequired()])
    Departure = StringField('출발 공항 코드', validators=[DataRequired()])
    Arrival = StringField('도착 공항 코드', validators=[DataRequired()])
    DepartureTime = DateField('종료 날짜', format='%h-%m-%s', validators=[DataRequired()])
    submit = SubmitField('검색')


class ChangeAirportStateDateRangeForm(FlaskForm):
    """
    Form for Change Airport State by date range, for staff_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    start_date = DateField('적용 시작 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('적용 종료 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    airportId = StringField('공항 번호', validators=[DataRequired()])
    submit = SubmitField('검색')


class ChangeAircraftStateDateRangeForm(FlaskForm):
    """
    Form for Change Aircraft State by date range, for staff_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    start_date = DateField('적용 시작 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    end_date = DateField('적용 종료 날짜', format='%Y-%m-%d', validators=[DataRequired()])
    prev_aircraftId = StringField('취소할 항공기 번호', validators=[DataRequired()])
    new_aircraftId = StringField('대체 항공기 번호', validators=[DataRequired()])
    submit = SubmitField('검색')


class RecordActualDepartureTime(FlaskForm):
    """
    Form for Recording Actual Departure Time, for staff_views.py
    Notes:
        start_date: start date for searching flights
        end_date: end date for searching flights
    """
    DailyFlightId = StringField('항공편 스케줄 번호(DailyFlightId, FL000)', validators=[DataRequired()])
    ActualDepartureDay = DateField('실제 출발 시간 입력(연/월/일)', format='%Y-%m-%d', validators=[DataRequired()])
    ActualDepartureTime = DateField('실제 출발 시간 입력(시/분/초)', format='%h-%m-%s', validators=[DataRequired()])
    submit = SubmitField('검색')
