from flask import Flask, jsonify
import socket
import os

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from AKS! (via ArgoCD GitOps + Trivy)",
        "hostname": socket.gethostname(),
        "version": APP_VERSION
    })

@app.route("/healthz")
def healthz():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
