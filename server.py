from app import app

from app.controllers.authors import authors
from app.controllers.books import books
from app.controllers.auth import auth

app.register_blueprint(auth)
app.register_blueprint(authors, url_prefix='/authors')
app.register_blueprint(books, url_prefix='/books')


if __name__ == '__main__':
    app.run(debug=True)
