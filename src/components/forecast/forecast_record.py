from components.forecast.forecast_data_gateway import db


class Forecast(db.Model):
    day = db.Column(db.String, nullable=False, primary_key=True)
    latitude = db.Column(db.Float, nullable=False, primary_key=True)
    longitude = db.Column(db.Float, nullable=False, primary_key=True)
    temperature = db.Column(db.Float, nullable=False)
    precipitation = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    cloud_coverage = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.Float, nullable=False)
    wind = db.Column(db.Float, nullable=False)
    wind_gust = db.Column(db.Float, nullable=False)
    dew_point = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Forecast "{self.latitude}, {self.longitude}">'
