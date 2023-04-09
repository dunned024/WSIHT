from datetime import datetime

import requests
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from herbie import Herbie

from forecast_record import Forecast

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Weather.sqlite3'


# db = SQLAlchemy(app)
# class Weather(db.Model):
#     datetime = db.Column(db.DateTime, primary_key=True, default=datetime.utcnow())
#     temperature = db.Column(db.Integer, nullable=False)


def get_temperature():
    H = Herbie("2023-04-04", model="hrrr", product="sfc", fxx=0)
    all_data = H.xarray(":surface:")

    all_data = H.xarray(":(?:(?:APCP|GUST|VIS):surface|(?:DPT|RH|TMP):2 m above ground|(?:WIND):10 m above ground|(?:TCDC):entire atmosphere):")

    # APCP : tp : accumulated/total precipitation (kg/m2)
    # GUST : gust : surface wind gust (m/s)
    # VIS : vis : visibility (m)
    surface = H.xarray(":(?:APCP|GUST|VIS):surface")
    
    # DPT : d2m : dew point temperature (degrees K)
    # RH : r2 : relative humidity (%)
    # TMP : t2m : temperature (degrees K)
    two_meters = H.xarray(":(?:DPT|RH|TMP):2 m above ground")

    # WIND : si10 : wind (m/s)
    ten_meters = H.xarray(":WIND:10 m above ground")

    # TCDC : tcc : total cloud coverage (%)
    atmosphere = H.xarray(":TCDC:entire atmosphere")

    Forecast.