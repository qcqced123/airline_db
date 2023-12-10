from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy import Table, insert, delete, select, and_
from werkzeug.utils import redirect
from app.forms import DateRangeForm

bp = Blueprint('user', __name__, url_prefix='/')


@bp.route('/search_airline/', methods=['GET', 'POST'])
def search():
    from app import engine, metadata_obj, database
    form = DateRangeForm()
    if request.method == 'POST' and form.validate_on_submit():
        error, start_date, end_date = None, form.start_date.data, form.end_date.data

        dailyFlight = Table("DailyFlight", metadata_obj, autoload_with=engine)
        result = select(dailyFlight).where(
            and_(dailyFlight.c.Date >= start_date, dailyFlight.c.Date <= end_date)
        ).order_by(dailyFlight.c.Date.asc())

        with engine.connect() as connection:
            result = connection.execute(result)
            flights = result.fetchall()
        return render_template('user/search_result.html', flights=flights)
    return render_template('user/search_airline.html', form=form)

