from flask import Blueprint, render_template, jsonify, request
from database import get_db_connection

shelf_page = Blueprint('shelf_page', __name__, template_folder='templates')  # Tworzymy blueprint dla tras związanych z półkami

@shelf_page.route("/shelf")
def shelf():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM shelf")
            shelves = cursor.fetchall()
    finally:
        connection.close()
    return render_template('shelf.html', shelves=shelves)

@shelf_page.route("/api/shelf", methods=["POST"])
def add_shelf():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            description = data['description']
            # Dodawanie nowej półki do bazy danych
            cursor.execute("INSERT INTO shelf (description) VALUES (%s)", (description,))
            connection.commit()
            return jsonify({'msg': 'Dodano nowy rekord'}), 201
    finally:
        connection.close()

@shelf_page.route("/api/shelf/<int:id>", methods=["PUT"])
def update_shelf(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            description = data['description']
            # Aktualizacja istniejącej półki w bazie danych
            cursor.execute("UPDATE shelf SET description = %s WHERE id = %s", (description, id))
            connection.commit()
            return jsonify({'msg': 'Zaktualizowano'}), 200
    finally:
        connection.close()

@shelf_page.route("/api/shelf/<int:id>", methods=["DELETE"])
def delete_shelf(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Usuwanie półki z bazy danych
            cursor.execute("DELETE FROM shelf WHERE id = %s", (id,))
            connection.commit()  # Zatwierdzamy transakcję
            return jsonify({'msg': 'Usunięto'}), 200
    finally:
        connection.close()
