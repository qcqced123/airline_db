from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy import Table, insert, delete, select, and_, text
from werkzeug.utils import redirect


bp = Blueprint('purchase', __name__, url_prefix='/')


@bp.route('/purchase/', methods=['GET', 'POST'])
def purchase():
    """ Concrete view for purchasing flight tickets """
    from app import engine, metadata_obj, database

    return render_template('purchase/reservation.html')


@bp.route('/reservation', methods=['POST'])
def reservation():
    """
    Concrete view for Displaying flight details, which is selected by user in search_result.html
    This view have 2 Parts:
        1. Displaying flight details, price of flight tickets of each seat class
        2. Displaying number of left seats of each seat class, breakdown by AircraftId
        3. Selecting class and record reservation table
        4. Select mileage payment or not
    """
    from app import engine, metadata_obj, database

    userId = session['user_id']
    userName = session['user_name']
    date = request.form['date']
    state = request.form['state']
    dailyFlightId = request.form['dailyFlightId']
    flightNumber = request.form['flightNumber']
    aircraftId = request.form['aircraftId']
    price_list = []  # economy class, business class
    cursor = engine.raw_connection().cursor()

    # 1. Displaying flight details, price of flight tickets of each seat class
    for is_business in [False, True]:
        cursor.execute(f"SELECT AirlineReservationWebDB.CalculateDiscountedPrice('{dailyFlightId}', '{userId}', {is_business});")
        # cursor.execute(query, (dailyFlightId, userId, is_business))
        result = cursor.fetchone()[0]
        price_list.append(result)  # 결과 가져오기

    # 2. Displaying number of left seats of each seat class, breakdown by AircraftId
    airCraft = Table("Aircraft", metadata_obj, autoload_with=engine)
    economy = select(airCraft.c.Economy).where(airCraft.c.AircraftId == aircraftId)
    business = select(airCraft.c.Business).where(airCraft.c.AircraftId == aircraftId)
    num_economy, num_business = database.execute(economy).scalar(), database.execute(business).scalar()
    return render_template(
        'purchase/reservation.html',
        userId=userId,
        userName=userName,
        date=date,
        state=state,
        dailyFlightId=dailyFlightId,
        flightNumber=flightNumber,
        aircraftId=aircraftId,
        economy_price=price_list[0],
        business_price=price_list[1],
        num_economy=num_economy,
        num_business=num_business
    )
