from app.models.connection import MySQLConnection
from flask import flash
from app.models.base_model import Base

MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `authors` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`))
    ENGINE = InnoDB;
''')

# tabla intermedia
MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `writes` (
    `author_id` int NOT NULL,
    `book_id` int NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (author_id, book_id),
    foreign key (author_id) references authors(id),
    foreign key (book_id) references books(id)
    )
''')

class Author(Base):

    table = 'authors'

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