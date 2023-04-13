from dotenv import load_dotenv
from flask import Blueprint, Flask, render_template

from components.hike.hike_application import hikes
from components.forecast.forecast_data_gateway import db
from components.forecast.forecast_record import Forecast


APP_NAME = "WSIHT"

index = Blueprint('index', APP_NAME, template_folder='src/templates')


@index.route('/')
def index_blueprint():
    return render_template('index.html')


def create_app():
    load_dotenv()

    app = Flask(APP_NAME)
    app.config.from_prefixed_env()

    db.init_app(app)
    with app.app_context():
        db.create_all()

    from components.forecast.forecast_collector import forecasts
    app.register_blueprint(index)
    app.register_blueprint(hikes)
    app.register_blueprint(forecasts)
    return app


if __name__ == "__main__":
    app = create_app()
