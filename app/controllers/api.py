from flask import session, redirect, render_template, Blueprint, request, jsonify
from app.models.book_model import Book
import json

api = Blueprint('api', __name__)

@api.route('/template')
def libros_ajax():
    return render_template('books_ajax.html')

@api.route('/books')
def books():
    books_dicts = Book.get_all()
    return jsonify(books=books_dicts)

# ['hola', 'chao'] => "['hola', 'chao']"
