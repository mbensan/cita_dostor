from app.models.connection import MySQLConnection
from flask import flash


class Base:

    table = 'none'

    @classmethod
    def get_all(cls):
        print('NOMBRE TABLA ' + cls.table)
        rows = MySQLConnection().query_db(f'select * from {cls.table}')
        return rows
    
    @classmethod
    def get_one(cls, id):
        data = {
            'table': cls.table,
            'id': id
        }
        query = 'select * from '+cls.table+' where id=%(id)s'
        rows = MySQLConnection().query_db(query, data)
        return rows[0]
    
    @classmethod
    def delete(cls, id):
        query = 'delete from '+cls.table+' where id=%(id)s'
        data = {
            'table': cls.table,
            'id': id
        }
        MySQLConnection().query_db(query, data)
        return 'Item eliminado'
