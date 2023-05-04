from flask import session, redirect, render_template, Blueprint, request, flash
from app.models.book_model import Book
from app.decorators import login_required

books = Blueprint('books', __name__)

@books.route('/')
@login_required
def home():
    books_dicts = Book.get_all()
    return render_template('books.html', books=books_dicts)


@books.route('/new', methods=['POST'])
def new():
    # 1. Recuperamos datos del formulario
    title = request.form['title']
    num_pages = request.form['num_pages']
    # 2. Validamos la entrada
    is_valid = Book.validate(request.form)
    # 3. Si el formulario no es válido, redirigimos de vuelta al template del formulario
    if not is_valid:
        return redirect('/books')

    # 4. Llamamos al modelo
    Book.add(title, num_pages)
    # 5. Flash con mensaje de ingreso exitoso
    flash(f'Libro {title} agregado con éxito', 'success')
    # 5. Redirigimos a ruta de libros
    return redirect('/books')
