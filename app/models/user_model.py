from flask import flash
from app.models.connection import MySQLConnection
from app import bcrypt


MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `world`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `password` VARCHAR(255) NOT NULL,
    `avatar` TEXT,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`))
    ENGINE = InnoDB;
''')

class User:
    
    # chequea si 'email' está o no disponible para crear un nuevo usuario
    @classmethod
    def is_email_free(cls, email):
        query = 'select * from users where email=%(email)s'
        data = {
            'email': email
        }

        results = MySQLConnection().query_db(query, data)
        if len(results) == 0:
            return True
        else:
            return False

    @classmethod
    def add(cls, name, email, password):
        # 1. Generamos una contraseña encriptada
        hashed_password = bcrypt.generate_password_hash(password)

        # 2. Generamos la query
        query = 'insert into users (name, email, password) values (%(name)s, %(email)s, %(password)s)'
        data = {
            'name': name,
            'email': email,
            'password': hashed_password
        }

        # 3. Ejecutamos la consulta
        new_user_id = MySQLConnection().query_db(query, data)
        return new_user_id
    
    # obtiene un usuario con su email y su password, o None
    @classmethod
    def get_with_credential(cls, email, password):
        # 1. Obtenemos el usuario
        query = 'select * from users where email=%(email)s'
        data = {
            'email': email
        }

        results = MySQLConnection().query_db(query, data)

        # 2. En caso que el usuario no exista
        if len(results) == 0:
            flash('Usuario Inexistente', 'danger')
            return None
        
        # 3. Revisar que password sea la correcta
        user = results[0]
        if not bcrypt.check_password_hash(user['password'], password):
            flash('Contraseña Incorrecta', 'danger')
            return None
        
        return user
