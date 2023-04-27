from flask import flash, redirect, session

def login_required(ruta):

    def wrapper(*args, **kwargs):
        if 'user' not in session or session['user'] is None:
            flash('No tienes accesos a esta página. FUERA DE AQUI!!!!', 'danger')
            return redirect('/login')
        resp = ruta(*args, **kwargs)
        return resp
    
    return wrapper
