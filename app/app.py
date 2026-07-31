from flask import Flask, jsonify, Response
import socket
import os
import time
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

REQUEST_COUNT = Counter("app_requests_total", "Total requests", ["endpoint"])
REQUEST_LATENCY = Histogram("app_request_latency_seconds", "Request latency", ["endpoint"])

@app.route("/")
def home():
    start = time.time()
    REQUEST_COUNT.labels(endpoint="/").inc()
    resp = jsonify({
        "message": "Hello from AKS! (via ArgoCD GitOps + Trivy)",
        "hostname": socket.gethostname(),
        "version": APP_VERSION
    })
    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)
    return resp

@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
