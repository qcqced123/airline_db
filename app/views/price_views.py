from flask import Blueprint, url_for, render_template, flash, request, current_app, jsonify
from app import db


bp = Blueprint('main', __name__, url_prefix='/')


@bp.route("/", methods=["POST"])
def get_total_booking_duty_free_price():
    """
    DutyFreeBooking 테이블에 기록된 유저별 구매 품목에 대한 총액 계산
    Args:
        userId: UserId, default str
    Returns:
        total_price: 총액, default int
    """
    userId = request.json["userId"]
    duty_free_bookings = db.session.query(
        db.DutyFreeBooking
    ).filter(db.DutyFreeBooking.userId == userId).all()

    total_price = 0
    for duty_free_booking in duty_free_bookings:
        total_price += duty_free_booking.amount

    return jsonify({"total_price": total_price})
