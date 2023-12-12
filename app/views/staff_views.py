from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, insert, delete, select, and_, text

from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app.forms import AddFlightDateRangeForm, ChangeAirportStateDateRangeForm, ChangeAircraftStateDateRangeForm, RecordActualDepartureTime

bp = Blueprint('staff', __name__, url_prefix='/')


@bp.route('/add_daily_flight', methods=('GET', 'POST'))
def add_daily_flight():
    """ Concrete view for adding daily flight """
    from app import engine, metadata_obj, database
    form = AddFlightDateRangeForm()
    return render_template(
        'staff/add_daily_flight.html',
        form=form,
    )


@bp.route('/apply_add_flight', methods=('GET', 'POST'))
def apply_add_flight():
    """ Concrete view for applying add flight """
    from app import engine, metadata_obj, database
    flightNumber = request.form['flightNumber']
    Departure = request.form['Departure']
    Arrival = request.form['Arrival']
    DepartureTime = request.form['DepartureTime']
    aircraftId = request.form['aircraftId']
    start_date = request.form['start_date']
    end_date = request.form['end_date']


    flightNumberTable = Table("FlightNumber", metadata_obj, autoload_with=engine)
    newFlightSchedule = insert(flightNumberTable).values(
        FlightNumber=flightNumber,
        DepartureAirportCode=Departure,
        ArrivalAirportCode=Arrival,
        DepartureTime=DepartureTime,
    )
    database.execute(newFlightSchedule)
    database.commit()

    database.execute(text("CALL CreateDailyFlights(:StartDate, :EndDate, :FlightNumber, :AircraftId)"),
                     {"StartDate": start_date,
                      "EndDate": end_date,
                      "FlightNumber": flightNumber,
                      "AircraftId": aircraftId})
    database.commit()
    flash("추가가 완료 되었습니다.")
    return redirect(url_for('main.staff'))


@bp.route('/change_aircraft_state', methods=('GET', 'POST'))
def change_aircraft_state():
    """ Concrete view for change aircraft state """
    from app import engine, metadata_obj, database
    form = ChangeAircraftStateDateRangeForm()
    database.execute(text("CALL DailyFlightAircraftChange(:StartDate, :EndDate, :PrevAircraftId, :NewAircraftId)"),
                     {"StartDate": form.start_date.data,
                      "EndDate": form.end_date.data,
                      "PrevAircraftId": form.prev_aircraftId.data,
                      "NewAircraftId": form.new_aircraftId.data})
    database.commit()
    flash("변경이 완료 되었습니다.")
    return render_template(
        'staff/change_aircraft_state.html',
        form=form,
    )


@bp.route('/change_airport_state', methods=('GET', 'POST'))
def change_airport_state():
    """ Concrete view for change airport state """
    from app import engine, metadata_obj, database
    form = ChangeAirportStateDateRangeForm()
    database.execute(text("CALL CancelFlights(:StartDate, :EndDate, :AirportCode)"),
                     {"StartDate": form.start_date.data,
                      "EndDate": form.end_date.data,
                      "AirportCode": form.airportId.data})
    database.commit()
    flash("공항 사용 불가 처리가 완료 되었습니다.")
    return render_template(
        'staff/change_airport_state.html',
        form=form,
    )


@bp.route('/departure', methods=('GET', 'POST'))
def departure():
    """ Concrete view for departure """
    from app import engine, metadata_obj, database
    form = RecordActualDepartureTime()
    return render_template(
        'staff/departure.html',
        form=form,
    )


@bp.route('/apply_departure', methods=('GET', 'POST'))
def apply_departure():
    """ Concrete view for applying departure """
    from app import engine, metadata_obj, database
    DailyFlightId = request.form['DailyFlightId']
    ActualDepartureDay = request.form['ActualDepartureDay']
    ActualDepartureTime = request.form['ActualDepartureTime']
    ActualDepart = ActualDepartureDay + " " + ActualDepartureTime

    ActualDepartTable = Table("ActualDepartureTime", metadata_obj, autoload_with=engine)
    newActualDepartureTime = insert(ActualDepartTable).values(
        DateTime=ActualDepart,
        DailyFlightId=DailyFlightId,
    )
    database.execute(newActualDepartureTime)
    database.commit()
    flash("기록이 완료되었습니다.")

    return redirect(url_for('main.staff'))
