from forecast_data_gateway import db

class Forecast(db.Model):
    latitude = db.Column(db.float)
    longitude = db.Column(db.float)
    temperature = db.Column(db.float)
    humidity = db.Column(db.float)
    cloud_coverage = db.Column(db.float)
    visibility = db.Column(db.float)
    wind = db.Column(db.float)
    wind_gust = db.Column(db.float)
    dew_point = db.Column(db.float)
