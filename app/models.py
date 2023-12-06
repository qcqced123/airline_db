from app import db


class User(db.Model):
    """ User Model for storing user related details
    Notes:
        id: User ID for login (아이디)
        username: User Name for display (이름)
        password: User Password for login (비밀번호)
    """
    user_id = db.Column(db.String(100), primary_key=True)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

