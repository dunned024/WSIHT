from prometheus_flask_exporter import PrometheusMetrics

metrics = PrometheusMetrics.for_app_factory()
metrics.info("WSIHT", "Application info", version="1.0.0")
