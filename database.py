import pymysql
from flask import Flask

app = Flask(__name__)

# Konfiguracja połączenia z bazą danych MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'biblioteka'

def get_db_connection():
    # Funkcja do ustanawiania i zwracania połączenia z bazą danych MySQL
    return pymysql.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        db=app.config['MYSQL_DB'],
        cursorclass=pymysql.cursors.DictCursor  #kursor słownikowegy by uzyskać wyniki jako słowniki
    )
