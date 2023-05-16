from flask import Flask
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)

app.config.from_pyfile('../config.py')
app.secret_key = app.config['SECRET_KEY']

bcrypt = Bcrypt(app)

# acá crearemos los filtros de Jinja2
@app.template_filter('fecha')
def fecha_esp (fecha):
    meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sept', 'Oct', 'Nov', 'Dic']
    mes = meses[fecha.month - 1]
    fecha_legible = f'{fecha.day} de {mes}, {fecha.year}'
    return fecha_legible


@app.template_filter('hora')
def hora_esp (hora):
    hoy = datetime(2010, 1, 1)
    hoy += hora

    return hoy.strftime('%H:%M')
