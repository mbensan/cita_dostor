from app.models.connection import MySQLConnection
from flask import flash

MySQLConnection().query_db('''
    CREATE TABLE IF NOT EXISTS `world`.`books` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `title` VARCHAR(255) NOT NULL,
    `num_pages` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT NOW(),
    `updated_at` DATETIME NOT NULL DEFAULT NOW(),
    PRIMARY KEY (`id`))
    ENGINE = InnoDB;
''')

class Book:

    @classmethod
    def validate(cls, form):
        # 0. Obtenemos los campos del formulario
        title = form['title'].strip()
        num_pages = form['num_pages'].strip()
        # 1. Partimos asumiendo que todos los valores del formulario son válidos
        is_valid = True
        # 2. Vamos validando uno a uno estos valores
        if len(title) < 3:
            flash('El título no puede medir menos que 3', 'danger')
            is_valid = False
        
        try:
            num_pages = int(num_pages)
        except ValueError:
            is_valid = False
            flash('El número de páginas debe ser un número entero', 'danger')
            return
        num_pages = int(num_pages)
        if num_pages < 1:
            flash('El número de páginas debe ser mayor a 1', 'danger')   
            is_valid = False  
        
        return is_valid

    @classmethod
    def get_all(cls):
        books = MySQLConnection().query_db('select * from books')
        return books
    

    @classmethod
    def add(cls, title, num_pages):
        query = 'insert into books (title, num_pages) values (%(title)s, %(num_pages)s)'
        data = {
            'title': title,
            'num_pages': int(num_pages)
        }

        new_book_id = MySQLConnection().query_db(query, data)
        return new_book_id
