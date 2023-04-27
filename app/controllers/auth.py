from flask import session, redirect, render_template, Blueprint, request, flash
from app.models.user_model import User
from app.decorators import login_required

auth = Blueprint('auth', __name__)

@auth.route('/')
@login_required
def home():
    return render_template('home.html')


@auth.route('/login')
def login_form():
    return render_template('auth.html')


@auth.route('/logout')
def logout():
    session['user'] = None
    return redirect('/login')


@auth.route('/register', methods=['POST'])
def register():
    # 1. Recuperamos los campos del formulario
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    pass_confirm = request.form['pass_confirm']

    # 2. Revisamos que ambas contraseñas coincidan
    if password != pass_confirm:
        flash('Las contraseñas no coinciden', 'danger')
        return redirect('/login')
    
    # 3. Revisamos que contraseña tenga al menos 6 caracteres
    if len(password) < 6:
        flash('La contraseña debe ser de largo al menos 6', 'danger')
        return redirect('/login')
    
    # 4. Verificamos que usuario no exista anteriormente
    if not User.is_email_free(email):
        flash('Ese correo ya está registrado', 'danger')
        return redirect('/login')
    
    # 5. Ingresamos el nuevo usuario
    new_user_id = User.add(name, email, password)

    # 6. Si todo está OK, guardamos al usuario en sesión
    session['user'] = {
        'name': name,
        'email': email,
        'id': new_user_id
    }
    # 7. Y redirigimos al HOME
    flash('Persona registrada con éxito', 'success')
    return redirect('/')


@auth.route('/login', methods=['POST'])
def login():
    # 1. Recuperamos los datos del formulario
    email = request.form['email']
    password = request.form['password']

    # 2. Recuperar al usuario desde la base de datos
    user = User.get_with_credential(email, password)

    # 3. Si el usuario es None, redirigimos al formulario de LOGIN
    if user is None:
        return redirect('/login')
    
    # 4. Creamos la sesión
    session['user'] = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email']
    }

    # 5. Lo mandamos al HOME
    return redirect('/')