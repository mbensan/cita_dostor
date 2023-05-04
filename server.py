from app import app

from app.controllers.authors import authors
from app.controllers.books import books
from app.controllers.auth import auth
from app.controllers.citas import citas
from app.controllers.weather import weather
from app.controllers.api import api

app.register_blueprint(auth)
app.register_blueprint(citas)
app.register_blueprint(authors, url_prefix='/authors')
app.register_blueprint(books, url_prefix='/books')
app.register_blueprint(weather, url_prefix='/weather')
app.register_blueprint(api, url_prefix='/api')


if __name__ == '__main__':
    app.run(
        debug=app.config['DEBUG'],
        port=app.config['PORT']
    )
