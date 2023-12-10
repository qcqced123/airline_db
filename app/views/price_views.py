from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify


bp = Blueprint('price', __name__, url_prefix='/')


@bp.route("/price/total-duty-free-price", methods=["POST"])
def get_total_duty_free_price(UserId: str):
    from app import db, engine, metadata_obj, database
    """
    Calculate the total for each recorded user's purchases (from DutyFreeBooking Table)
    Args:
        UserId: UserId, default str
    Returns:
        total_price: breakdown by userid, default int
    """
    userId = request.json[UserId]
    duty_free_bookings = db.session.query(
        db.DutyFreeBooking
    ).filter(db.DutyFreeBooking.userId == userId).all()

    total_price = 0
    for duty_free_booking in duty_free_bookings:
        total_price += duty_free_booking.amount
    print(total_price)
    return jsonify({"total_price": total_price})


@bp.route('/calculate_discounted_price', methods=['POST'])
def calculate_discounted_price():
    try:
        input_data = request.get_json()

        input_daily_flight_id = input_data['inputDailyFlightId']
        input_user_id = input_data['inputUserId']
        is_business = input_data['isBusiness']

        if input_user_id not in UserTable or input_daily_flight_id not in PriceTable:
            return jsonify({"error": "Invalid User ID or Daily Flight ID"}), 400

        discount_rate = UserTable[input_user_id]["DiscountId"]
        class_key = "Business" if is_business else "Economy"
        base_price = PriceTable[input_daily_flight_id][class_key]

        discounted_price = base_price * (1 - discount_rate)

        return jsonify({"output": f"Discounted price for {input_user_id} on {input_daily_flight_id}: ${discounted_price:.2f}"}), 200

    except KeyError:
        return jsonify({"error": "Missing required fields"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
