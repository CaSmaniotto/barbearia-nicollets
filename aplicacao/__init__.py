from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///barbearia.db"
app.config["SECRET_KEY"] = "SECRET_KEY"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app, name='Gerenciador', template_mode='bootstrap3')

login_manager = LoginManager(app)
login_manager.login_message = "Por favor faça login para acessar essa página!"

login_manager.login_view = "home"
login_manager.refresh_view = 'home'

from aplicacao import routes