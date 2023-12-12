from datetime import datetime
from sqlalchemy.orm import sessionmaker
from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy import Table, insert, update, delete, select, and_, text
from werkzeug.utils import redirect
from app.forms import DutyFreeFrom, SpecialInfoFrom

bp = Blueprint('purchase', __name__, url_prefix='/')


def generate_reservation_id(database: sessionmaker, reservation: Table) -> str:
    """ Generate ReservationId """
    query = select(reservation.c.ReservationId).order_by(reservation.c.ReservationId.desc()).limit(1)
    last_reservation_id = database.execute(query).scalar()

    if last_reservation_id:
        reservation_id_number = int(last_reservation_id[2:]) + 1
        reservation_id = 'RV' + str(reservation_id_number).zfill(4)
        return reservation_id
    else:
        return 'RV0001'


def get_current_time() -> str:
    """ Get current time """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


@bp.route('/duty_free/apply/', methods=['GET', 'POST'])
def record():
    """ Concrete view for recording duty free shopping list for each user """
    from app import engine, metadata_obj, database
    itemId = request.form['itemId']
    itemName = request.form['itemName']
    quantity = request.form['quantity']
    totalPrice = request.form['totalPrice']
    userId = request.form['userId']
    dailyFlightId = request.form['dailyFlightId']

    dutyFreePayment = Table("DutyFreeBooking", metadata_obj, autoload_with=engine)
    dutyFree = insert(dutyFreePayment).values(Date=get_current_time(), DailyFlightId=dailyFlightId, UserId=userId, ItemId=itemId, Amount=quantity)
    database.execute(dutyFree)
    database.commit()
    return redirect(url_for('main.personal'))


@bp.route('/duty_free/total/', methods=['GET', 'POST'])
def total():
    from app import engine, metadata_obj, database
    itemId = request.form['itemId']
    quantity = request.form['quantity']
    userId = request.form['userId']
    dailyFlightId = request.form['dailyFlightId']

    dutyFreeTable = Table("DutyFreeGoods", metadata_obj, autoload_with=engine)
    itemName = select(dutyFreeTable.c.ItemName).where(dutyFreeTable.c.ItemId == itemId)
    itemPrice = select(dutyFreeTable.c.Price).where(dutyFreeTable.c.ItemId == itemId)
    itemName, item_price = database.execute(itemName).scalar(), database.execute(itemPrice).scalar()
    totalPrice = int(item_price) * int(quantity)
    return render_template(
        'purchase/total_duty_free.html',
        itemId=itemId,
        itemName=itemName,
        quantity=quantity,
        totalPrice=totalPrice,
        userId=userId,
        dailyFlightId=dailyFlightId
    )


@bp.route('/duty_free', methods=['GET', 'POST'])
def duty_free():
    """ Concrete view for duty free shopping """
    from app import engine, metadata_obj, database
    userId = request.form['userId']
    dailyFlightId = request.form['dailyFlightId']

    dutyFreeTable = Table("DutyFreeGoods", metadata_obj, autoload_with=engine)
    itemList = database.execute(select(dutyFreeTable)).fetchall()

    form = DutyFreeFrom()
    return render_template(
        'purchase/dutyfree.html',
        form=form,
        itemList=itemList,
        userId=userId,
        dailyFlightId=dailyFlightId
    )


@bp.route('/special_info_result/', methods=['GET', 'POST'])
def special_info_result():
    """ Concrete view for applying convenience information of user """
    from app import engine, metadata_obj, database
    userId = request.form['userId']
    userName = request.form['userName']
    dailyFlightId = request.form['dailyFlightId']
    specialInfoId = request.form['specialInfoId']
    specialInfoTable = Table("SpecialInfoHistory", metadata_obj, autoload_with=engine)
    specialInfo = insert(specialInfoTable).values(
        DailyFlightId=dailyFlightId, UserId=userId, SpecialInfoId=specialInfoId
    )
    database.execute(specialInfo)
    database.commit()
    return render_template(
        'purchase/special_info_result.html',
        userId=userId,
        userName=userName,
        dailyFlightId=dailyFlightId,
    )


@bp.route('/convenienceInfo/', methods=['GET', 'POST'])
def convenience_info():
    """
    Concrete view for Displaying convenience information of user
    This view have 2 Parts:
        1. apply payment by mileage or add mileage from payment by cash
        2. Select Convenience information
    """
    from app import engine, metadata_obj, database
    seat = request.form['seat']
    userId = request.form['userId']
    userName = request.form['userName']
    dailyFlightId = request.form['dailyFlightId']
    payment = request.form['payment']

    # 1. apply payment by mileage or add mileage from payment by cash
    userTable = Table("User", metadata_obj, autoload_with=engine)
    if payment == "Milage":
        payment_milage = request.form['payment_milage']
        userMilage = update(userTable).where(userTable.c.UserId == userId).values(UserMileageValue=userTable.c.UserMileageValue - payment_milage)
        database.execute(userMilage)
    else:
        earn_milage = request.form['earn_milage']
        userMilage = update(userTable).where(userTable.c.UserId == userId).values(UserMileageValue=userTable.c.UserMileageValue + earn_milage)
        database.execute(userMilage)
    database.commit()
    currMilage = select(userTable.c.UserMileageValue).where(userTable.c.UserId == userId)
    curr_milage = database.execute(currMilage).scalar()

    # 2. Select Convenience information
    specialInfo = Table("SpecialInfo", metadata_obj, autoload_with=engine)
    special_info_list = database.execute(select(specialInfo)).fetchall()

    form = SpecialInfoFrom()
    return render_template(
            'purchase/convenienceInfo.html',
            seat=seat,
            dailyFlightId=dailyFlightId,
            userId=userId,
            userName=userName,
            curr_milage=curr_milage,
            special_info_list=special_info_list,
            payment=payment,
            form=form
    )


@bp.route('/payment/', methods=['GET', 'POST'])
def payment():
    """
    Concrete view for Selecting Payment flight tickets
    This view have 2 Parts:
        1. record reservation table
        2. Select mileage payment or not
    """
    from app import engine, metadata_obj, database
    seat = request.form['seat']
    userId = request.form['userId']
    userName = request.form['userName']
    dailyFlightId = request.form['dailyFlightId']

    # 1. recording reservation table
    reservationTable = Table("Reservation", metadata_obj, autoload_with=engine)
    reservationId = generate_reservation_id(database, reservationTable)
    reservation = insert(reservationTable).values(
        ReservationId=reservationId,
        DailyFlightId=dailyFlightId,
        UserId=userId,
        AirlineCode='OZ',
        Class=seat
    )
    database.execute(reservation)
    database.commit()

    # 2. Select mileage payment or not
    userTable = Table("User", metadata_obj, autoload_with=engine)
    userMilage = select(userTable.c.UserMileageValue).where(userTable.c.UserId == userId)
    user_milage = database.execute(userMilage).scalar()

    flightMilage = Table("MileageUsage", metadata_obj, autoload_with=engine)
    economyMilage = select(flightMilage.c.Economy).where(flightMilage.c.DailyFlightId == dailyFlightId)
    businessMilage = select(flightMilage.c.Business).where(flightMilage.c.DailyFlightId == dailyFlightId)
    economy_milage, business_milage = database.execute(economyMilage).scalar(), database.execute(businessMilage).scalar()
    payment_milage = economy_milage if seat == 'Economy' else business_milage

    # 3. payment by only cash
    priceTable = Table("Price", metadata_obj, autoload_with=engine)
    earnMilageTable = Table("MileageEarn", metadata_obj, autoload_with=engine)

    economyPrice = select(priceTable.c.Economy).where(priceTable.c.DailyFlightId == dailyFlightId)
    businessPrice = select(priceTable.c.Business).where(priceTable.c.DailyFlightId == dailyFlightId)
    economy_price, business_price = database.execute(economyPrice).scalar(), database.execute(businessPrice).scalar()
    payment_cash = economy_price if seat == 'Economy' else business_price

    earnEconomyMilage = select(earnMilageTable.c.Economy).where(earnMilageTable.c.DailyFlightId == dailyFlightId)
    earnBusinessMilage = select(earnMilageTable.c.Business).where(earnMilageTable.c.DailyFlightId == dailyFlightId)
    earn_economy_milage, earn_business_milage = database.execute(earnEconomyMilage).scalar(), database.execute(earnBusinessMilage).scalar()
    earn_milage = earn_economy_milage if seat == 'Economy' else earn_business_milage

    return render_template(
        'purchase/payment.html',
        seat=seat,
        dailyFlightId=dailyFlightId,
        userId=userId,
        userName=userName,
        user_milage=user_milage,
        payment_milage=payment_milage,
        payment_cash=payment_cash,
        earn_milage=earn_milage
    )


@bp.route('/reservation', methods=['POST'])
def reservation():
    """
    Concrete view for Displaying flight details, which is selected by user in search_result.html
    This view have 2 Parts:
        1. Displaying flight details, price of flight tickets of each seat class
        2. Displaying number of left seats of each seat class, breakdown by AircraftId

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
