from flask import Blueprint, render_template, jsonify, request
from database import get_db_connection

book_page = Blueprint('book_page', __name__,
                      template_folder='templates')  # Tworzymy blueprint dla tras związanych z książkami


@book_page.route("/book")
def book():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Wykonujemy zapytanie SQL, aby pobrać wszystkie książki wraz z danymi autora i półki
            cursor.execute("""
                SELECT book.id, book.title, book.year, author.firstname, author.lastname, shelf.description
                FROM book
                JOIN author ON book.author_id = author.id
                JOIN shelf ON book.shelf_id = shelf.id
            """)
            books = cursor.fetchall()
    finally:
        connection.close()
    return render_template('book.html', books=books)


@book_page.route("/api/book", methods=["POST"])
def add_book():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            title = data['title']
            year = data['year']
            author_id = data['author_id']
            shelf_id = data['shelf_id']
            # Dodawanie nowej książki do bazy danych
            cursor.execute("INSERT INTO book (title, year, author_id, shelf_id) VALUES (%s, %s, %s, %s)",
                           (title, year, author_id, shelf_id))
            connection.commit()  # Zatwierdzamy transakcję
            return jsonify({'msg': 'Dodano nowy rekord'}), 201
    finally:
        connection.close()


@book_page.route("/api/book/<int:id>", methods=["PUT"])
def update_book(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            title = data['title']
            year = data['year']
            author_id = data['author_id']
            shelf_id = data['shelf_id']
            # Aktualizacja istniejącej książki w bazie danych
            cursor.execute("UPDATE book SET title = %s, year = %s, author_id = %s, shelf_id = %s WHERE id = %s",
                           (title, year, author_id, shelf_id, id))
            connection.commit()  # Zatwierdzamy transakcję
            return jsonify({'msg': 'Zaktualizowano'}), 200
    finally:
        connection.close()

@book_page.route("/api/book/<int:id>", methods=["DELETE"])
def delete_book(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Usuwanie książki z bazy danych
            cursor.execute("DELETE FROM book WHERE id = %s", (id,))
            connection.commit()  # Zatwierdzamy transakcję
            return jsonify({'msg': 'Usunięto'}), 200
    finally:
        connection.close()

@book_page.route("/api/book/related-data", methods=["GET"])
def get_related_data():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Pobieranie danych powiązanych autorów i półek
            cursor.execute("SELECT id, firstname, lastname FROM author")
            authors = cursor.fetchall()
            cursor.execute("SELECT id, description FROM shelf")
            shelves = cursor.fetchall()
    finally:
        connection.close()
    # Zwracanie danych powiązanych jako JSON
    return jsonify({'authors': authors, 'shelves': shelves})
