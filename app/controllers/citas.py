from flask import session, redirect, render_template, Blueprint, request, flash
from app.decorators import login_required
from app.models.cita_model import Cita
from datetime import datetime

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


UPLOAD_FOLDER = 'examenes'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']


@citas.route('/new-cita', methods=['POST'])
def create_cita():
    if not Cita.validate(request.form):
        return redirect('/new-cita')
    
    archivo = request.files['examenes']
    filename = archivo.filename
    ext = filename.split('.')[-1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        flash('Este formato no se permite', 'danger')
        return redirect('/new-cita')
    
    new_filename = datetime.now().strftime('%Y-%m-%d') + '_' + session['user']['name'] + '.' + ext
    archivo.save('examenes/' + new_filename)
    
    
    fecha = request.form.get('fecha', '').strip()
    hora = request.form.get('hora', '').strip()
    sintomas = request.form.get('sintomas', '').strip()
    paciente_id = request.form.get('paciente_id', '').strip()

    Cita.add(fecha, hora, sintomas, paciente_id, new_filename)

    return redirect('/')

