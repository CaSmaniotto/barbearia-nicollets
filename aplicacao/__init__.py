from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///barbearia.db"
app.config["SECRET_KEY"] = "SECRET_KEY"

database = SQLAlchemy(app)

admin = Admin(app, name='Gerenciador', template_mode='bootstrap3')

from aplicacao import routes