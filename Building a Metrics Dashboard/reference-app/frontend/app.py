from flask import Flask, json, render_template
from prometheus_flask_exporter import PrometheusMetrics
import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing

logging.basicConfig(level=logging.INFO)
logging.info("LOGLEVEL INFO")

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info("app_info", version="1.0.0")

config = Config(
    config={
        'sampler':
        {'type': 'const',
         'param': 1},
                        'logging': True,
                        'reporter_batch_size': 1,}, 
                        service_name="service")
jaeger_tracer = config.initialize_tracer()
tracing = FlaskTracing(jaeger_tracer, True, app)

@app.route('/')
def homepage():
    return render_template("main.html")

@app.route('/healthz')
def healthcheck():
    response = app.response_class(
            response=json.dumps({"result":"OK - healthy"}),
            status=200,
            mimetype='application/json'
        )
    return response


if __name__ == "__main__":
    app.run()