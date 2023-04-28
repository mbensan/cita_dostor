from flask import flash, session
from app.models.connection import MySQLConnection
from datetime import datetime
import time


MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `citas` (
    `id` INT NOT NULL AUTO_INCREMENT,
    fecha datetime not null,
    hora time not null,
    sintomas text not null,
    paciente_id int not null,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`),
    foreign key (paciente_id) references users(id))
    ENGINE = InnoDB;
''')

class Cita:
    
    @classmethod
    def validate (cls, form):
        is_valid = True

        fecha = form.get('fecha', '').strip()
        hora = form.get('hora', '').strip()
        sintomas = form.get('sintomas', '').strip()
        paciente_id = form.get('paciente_id', '').strip()

        # 1. Validamos la fecha
        try:
            fecha = datetime.strptime(fecha, '%Y-%m-%d').date()
            hoy = datetime.now().date()

            if fecha <= hoy:
                flash('Debe elegir una fecha a partir de mañana', 'danger')
                is_valid = False
        except ValueError:
            is_valid = False
            flash('La fecha debe estar en un formato válido', 'danger')

        
        # 2. Validamos la hora
        if hora == '':
            flash('Debe ingresar una hora', 'danger')
            is_valid = False
        elif hora <= '08:00' or hora >= '17:00':
            flash('la hora debe estar entre 8:00 y 17:00', 'danger')
            is_valid = False
        
        if len(sintomas) <= 3:
            flash('Los sintomas deben tener al menos 4 caracteres', 'danger')
            is_valid = False

        
        return is_valid
    
    @classmethod
    def add(cls, fecha, hora, sintomas, paciente_id):
        # 2. Generamos la query
        query = 'insert into citas (fecha, hora, sintomas, paciente_id) values (%(fecha)s, %(hora)s, %(sintomas)s, %(paciente_id)s)'
        data = {
            'fecha': fecha,
            'hora': hora,
            'sintomas': sintomas,
            'paciente_id': paciente_id
        }
        # Validamos que no existan otras 3 citas en la fecha
        otras_citas = cls.get_by_fecha(fecha)
        if len(otras_citas) >= 3:
            flash('No se pudo agregar la Cita. Ya existen otras 3 en la misma fecha', 'danger')
            return

        # 3. Ejecutamos la consulta
        new_cita_id = MySQLConnection().query_db(query, data)
        flash('Cita Creada', 'success')
        return new_cita_id
    
    @classmethod
    def get_all(cls):
        query = 'select * from citas join users on citas.paciente_id = users.id order by fecha desc'
        results = MySQLConnection().query_db(query)
        #print(results)
        return results
    
    @classmethod
    def get_by_fecha(cls, fecha):
        query = 'select * from citas where fecha=%(fecha)s'
        data = {'fecha': fecha}
        results = MySQLConnection().query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def delete(cls, id):
        # 1. Primero verificamos que la cita efectivamente exista
        cita = cls.get_one(id)
        if cita is None:
            return
        
        # 2. Verificamos que la cita efectivamente pertenezca al usuario que está logueado
        if cita['paciente_id'] != session['user']['id']:
            return

        # Finalmente borramos la cita
        id = int(id)
        query = 'delete from citas where id=%(id)s'
        data = {
            'id': id
        }

        # 3. Ejecutamos la consulta
        MySQLConnection().query_db(query, data)
    
    @classmethod
    def get_one(cls, id):
        id = int(id)

        query = 'select * from citas where id=%(id)s'
        data = {
            'id': id
        }

        #  Ejecutamos la consulta
        results = MySQLConnection().query_db(query, data)
        if len(results) > 0:
            return results[0]
        else:
            return None
