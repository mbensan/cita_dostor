import pymysql
from app import app

class MySQLConnection:

    def __init__(self):
        # cambiar el usuario y la contraseña según sea necesario
        connection = pymysql.connect(host = app.config['DB_HOST'],
            user = app.config['DB_USER'], 
            password = app.config['DB_PASSWORD'], 
            db = app.config['DB_NAME'],
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor,
            autocommit = True
        )
        # establecer la conexión a la base de datos
        self.connection = connection

    # el método para consultar la base de datos
    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # las consultas INSERT devolverán el NÚMERO DE ID de la fila insertada
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # las consultas SELECT devolverán los datos de la base de datos como una LISTA DE DICCIONARIOS
                    result = cursor.fetchall()
                    return result
                else:
                    # las consultas UPDATE y DELETE no devolverán nada
                    self.connection.commit()
            except Exception as e:
                # si la consulta falla, el método devolverá FALSE
                print("Something went wrong", e)
                return False
            finally:
                # cerrar la conexión
                self.connection.close()

''' Forma de usar el objeto Connection
rows = MySQLConnection().query_db('select * from countries where id=%(id)s', {'id': '2'})
print(rows)
'''