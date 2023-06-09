#!/usr/bin/env python

import io
import math
import os
from datetime import datetime
from urllib import parse

import xarray
from flask import Flask
from herbie import Herbie
from dotenv import load_dotenv

from components.forecast.forecast_record import Forecast
from components.forecast.forecast_data_gateway import db


COLUMNS = [c.name for c in Forecast.__table__.columns]
RENAME_MAP = {
    "time": "day",
    "t2m": "temperature",
    "tp": "precipitation",
    "r2": "humidity",
    "tcc": "cloud_coverage",
    "vis": "visibility",
    "si10": "wind",
    "gust": "wind_gust",
    "d2m": "dew_point",
}


def get_forecasts():
    today = datetime.today().strftime("%Y-%m-%d")

    print("erasing old data...")
    _delete_old_rows()

    print(f"gathering data for {today}...")
    all_data = _get_herbie_data(today)

    print("uploading chunks...")
    CHUNK_SIZE = 50
    total_chunks = math.ceil(len(all_data.x) / CHUNK_SIZE)
    for i, chunk in enumerate(_chunk_by_x(all_data, CHUNK_SIZE)):
        print(f"chunk: {i+1} / {total_chunks}")
        _upload_chunk(chunk)

    print("finished uploading data")
    return "success"


def _delete_old_rows():
        Forecast.query.delete()
        db.session.commit()


def _get_herbie_data(today: str):
    H = Herbie(today, model="hrrr", product="sfc", fxx=0)

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

    print("merging dataset...")
    all_data = xarray.merge([surface, two_meters, ten_meters, atmosphere], compat="override")

    # Measure from prime meridian
    all_data["longitude"] = all_data["longitude"] - 360
    return all_data.reset_coords(["latitude", "longitude", "time"])


def _chunk_by_x(all_data, chunk_size):
    return (all_data.sel(x=slice(pos, pos + chunk_size)) for pos in range(0, len(all_data.x), chunk_size))


def _upload_chunk(chunk):
    df = chunk.to_dataframe().rename(columns=RENAME_MAP)[COLUMNS]

    output = io.StringIO()
    df.to_csv(output, sep="\t", header=False, index=False)
    output.seek(0)

    conn = db.engine.raw_connection()
    cur = conn.cursor()
    cur.copy_from(output, "forecast", null="")
    conn.commit()
    cur.close()


if __name__ == "__main__":
    load_dotenv()
    app = Flask("forecast_collector")
    db_url = parse.urlsplit(os.getenv("DATABASE_URL", ""))
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://" + db_url.netloc + db_url.path

    db.init_app(app)
    with app.app_context():
        db.create_all()
        get_forecasts()
