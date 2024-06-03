from flask import Flask, render_template
from templates.appy2 import author_page
from book import book_page
from shelf import shelf_page  # Importujemy blueprint dla półek
from database import get_db_connection

app = Flask(__name__)  # Inicjalizujemy aplikację Flask
app.register_blueprint(author_page)  # Rejestrujemy blueprint dla autorów
app.register_blueprint(book_page)  # Rejestrujemy blueprint dla książek
app.register_blueprint(shelf_page, url_prefix='/')  # Rejestrujemy blueprint dla półek z prefiksem URL

@app.route('/')
def index():
    # Łączenie z bazą danych
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # pobieramy półki
            cursor.execute("SELECT * FROM shelf")
            shelves = cursor.fetchall()
    finally:
        connection.close()  # Zamykanie połączenia z bazą danych
    # Strona startowa
    return render_template('shelf.html', shelves=shelves)

if __name__ == '__main__':
    app.run(debug=True)  # Flask w debugu
