#!/usr/bin/env python3
import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'


db = SQLAlchemy(app)
class Weather(db.Model):
    datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
    temperature = db.Column(db.Integer, nullable=False)


def get_temperature():
    response = requests.get("https://weatherdbi.herokuapp.com/data/weather/boulder")
    return response.json()["currentConditions"]["temp"]["c"]


if __name__ == "__main__":
    current_temperature = get_temperature()
    new_entry = Weather(temperature=current_temperature)
    db.session.add(new_entry)
    db.session.commit()