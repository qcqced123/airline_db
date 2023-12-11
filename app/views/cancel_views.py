from datetime import datetime
from flask import Blueprint, url_for, render_template, flash
from flask import request, current_app, jsonify, session
from sqlalchemy import Table, insert, update, delete, select, and_, text
from werkzeug.utils import redirect


bp = Blueprint('cancel', __name__, url_prefix='/')


@bp.route('/init/', methods=['GET', 'POST'])
def cancel():
    """ Re-iniitalize all information, which is got from user input """
    from app import engine, metadata_obj, database
    userId = request.form['userId']
    dailyFlightId = request.form['dailyFlightId']
    cursor = engine.raw_connection().cursor()
    cursor.callproc('Deletionofpreorders', [userId, dailyFlightId])
    cursor.close()

    return redirect(url_for('main.personal'))
