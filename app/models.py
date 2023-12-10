from app import db, engine, metadata_obj, database


class AddUser(db.Model):
    """
    User Model for storing user related details
    Notes:
        id: User ID for login (아이디)
        username: User Name for display (이름)
        password: User Password for login (비밀번호)
    """
    user_id = database.Column(database.String(100), primary_key=True)
    user_name = database.Column(database.String(150), unique=True, nullable=False)
    password = database.Column(database.String(200), nullable=False)

