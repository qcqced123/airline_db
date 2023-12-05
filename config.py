db = {
    'user': 'root',
    'password': 'epqptjf!',
    'host': 'dbbook.cien.or.kr',
    'port': 53306,
    'database': 'AirlineReservationWebDB'
}
DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8mb4"
