import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine, MetaData, Table, Column, Float
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

meta = MetaData()

forecast = Table('forecast', meta,
    Column('latitude', Float, nullable=False),
    Column('longitude', Float, nullable=False),
    Column('temperature', Float, nullable=False),
    Column('humidity', Float, nullable=False),
    Column('cloud_coverage', Float, nullable=False),
    Column('visibility', Float, nullable=False),
    Column('wind', Float, nullable=False),
    Column('wind_gust', Float, nullable=False),
    Column('dew_point', Float, nullable=False),
)

with app.app_context():
    db.create_all()
