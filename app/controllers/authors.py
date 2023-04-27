from flask import session, redirect, render_template, Blueprint, request, flash
from app.models.author_model import Author
from app.decorators import login_required

authors = Blueprint('authors', __name__)

@authors.route('/')
@login_required
def home():
    authors_dicts = Author.get_all()
    #return render_template('countries.html', countries=countries_dicts)
    return render_template('authors.html', authors=authors_dicts)

@authors.route('/new', methods=['POST'])
def new():
    # 1. Recuperamos datos del formulario
    name = request.form['name']
    # 2. Validamos la entrada
    is_valid = Author.validate(request.form)
    # 3. Si el formulario no es válido, redirigimos de vuelta al template del formulario
    if not is_valid:
        return redirect('/authors')

    # 4. Llamamos al modelo
    Author.add(name)
    # 5. Flash con mensaje de ingreso exitoso
    flash(f'Autor {name} agregado con éxito', 'success')
    # 5. Redirigimos a ruta de autores
    return redirect('/authors')
