from flask import Flask

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


# Name that will appear in Jaeger
resource = Resource.create({
    "service.name": "flask-app"
})

# OpenTelemetry trace provider
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

# Send traces to Jaeger using OTLP/HTTP
exporter = OTLPSpanExporter(
    endpoint="http://127.0.0.1:4318/v1/traces"
)

provider.add_span_processor(
    SimpleSpanProcessor(exporter)
)


app = Flask(__name__)

# Automatically instrument all Flask routes
FlaskInstrumentor().instrument_app(app)


@app.route("/")
def home():
    return "Flask application with OpenTelemetry"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
