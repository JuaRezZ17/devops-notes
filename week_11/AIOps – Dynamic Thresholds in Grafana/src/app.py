from flask import Flask, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

http_requests_total = Counter(
    "http_requests_total",
    "Total number of HTTP requests"
)

@app.route("/")
def home():
    http_requests_total.inc()
    return "Demo app is running\n"

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

app.run(host="0.0.0.0", port=8000)