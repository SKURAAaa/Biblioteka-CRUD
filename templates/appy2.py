from flask import Blueprint, render_template, jsonify, request
from database import get_db_connection

author_page = Blueprint('author_page', __name__, template_folder='templates')

@author_page.route("/author")
def author():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM author")
            authors = cursor.fetchall()
    finally:
        connection.close()
    return render_template('author.html', authors=authors)

@author_page.route("/api/author", methods=["POST"])
def add_author():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            firstname = data['firstname']
            lastname = data['lastname']
            cursor.execute("INSERT INTO author (firstname, lastname) VALUES (%s, %s)", (firstname, lastname))
            connection.commit()
            return jsonify({'msg': 'Dodano nowy rekord'}), 201
    finally:
        connection.close()

@author_page.route("/api/author/<int:id>", methods=["PUT"])
def update_author(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            data = request.json
            firstname = data['firstname']
            lastname = data['lastname']
            cursor.execute("UPDATE author SET firstname = %s, lastname = %s WHERE id = %s", (firstname, lastname, id))
            connection.commit()
            return jsonify({'msg': 'Zaktualizowano'}), 200
    finally:
        connection.close()

@author_page.route("/api/author/<int:id>", methods=["DELETE"])
def delete_author(id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM author WHERE id = %s", (id,))
            connection.commit()
            return jsonify({'msg': 'Usunięto'}), 200
    finally:
        connection.close()
