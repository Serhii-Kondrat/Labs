from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.secret_key = b"secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

migrate = Migrate(app,db)

"""class User(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    name = Mapped[str] = mapped_column(db.String, nullable=False)
   #зробити для цього - password = db.Column(db.String(20))

"""
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    password = db.Column(db.String(20))


#from app import views

