from flask import session, redirect, render_template, Blueprint, request, flash
from app.decorators import login_required
from app.models.cita_model import Cita

citas = Blueprint('citas', __name__)


@citas.route('/new-cita')
@login_required
def create_form():
    return render_template('new_cita.html')


@citas.route('/delete-cita/<id>')
def delete(id):
    Cita.delete(id)
    flash('Cita eliminada', 'warning')
    return redirect('/')


@citas.route('/new-cita', methods=['POST'])
def create_cita():
    if not Cita.validate(request.form):
        return redirect('/new-cita')
    
    fecha = request.form.get('fecha', '').strip()
    hora = request.form.get('hora', '').strip()
    sintomas = request.form.get('sintomas', '').strip()
    paciente_id = request.form.get('paciente_id', '').strip()

    Cita.add(fecha, hora, sintomas, paciente_id)

    return redirect('/')

