from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy() # creating an instance of database
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__) # creating an instance of flask
    app.config['SECRET_KEY'] = 'super secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # initializing database
    db.init_app(app) 

    # importing blueprints
    from .views import views
    from .auth import auth
    # defining blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # importing models
    from .models import User, Post

    create_database(app)

    # creating an instance of login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    # telling flask how to manage login of users
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app): # only creates new database if it doesn't exist yet
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Database created successfully')

