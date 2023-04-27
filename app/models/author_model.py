from app.models.connection import MySQLConnection
from flask import flash

MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `authors` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`))
    ENGINE = InnoDB;
''')

class Author:

    @classmethod
    def validate(cls, form):
        # 0. Obtenemos los campos del formulario
        name = form['name'].strip()
        # 1. Partimos asumiendo que todos los valores del formulario son válidos
        is_valid = True
        # 2. Vamos validando uno a uno estos valores
        if len(name) < 3:
            flash('El nombre no puede medir menos que 3', 'danger')
            is_valid = False
        elif any(char.isdigit() for char in name):
            flash('El nombre no puede tener números', 'danger')
            is_valid = False
        
        return is_valid

    @classmethod
    def get_all(cls):
        authors = MySQLConnection().query_db('select * from authors')
        return authors
    
    @classmethod
    def get_one(cls, id):
        query = 'select * from countries where id=%(id)s'
        data = {
            'id': id
        }
        countries = MySQLConnection().query_db(query, data)
        return countries[0]
    
    @classmethod
    def get_with_cities(cls, id):
        country = cls.get_one(id)
        query = 'select * from cities where country_id=%(id)s'
        data = {
            'id': id
        }
        cities = MySQLConnection().query_db(query, data)
        country['cities'] = cities
        print(country)
        return country
    
    @classmethod
    def delete(cls, id):
        query = 'delete from countries where id=%(id)s'
        data = {
            'id': id
        }
        MySQLConnection().query_db(query, data)
        return 'País eliminado'
    
    @classmethod
    def add(cls, name):
        query = 'insert into authors (name) values (%(name)s)'
        data = {
            'name': name
        }

        new_author_id = MySQLConnection().query_db(query, data)
        return new_author_id
    

    @classmethod
    def edit(cls, id, name, gdp, population):
        query = 'update countries set name=%(name)s, gdp=%(gdp)s, population=%(population)s where id=%(id)s'
        data = {
            'id': id,
            'name': name,
            'gdp': gdp,
            'population': population
        }

        MySQLConnection().query_db(query, data)