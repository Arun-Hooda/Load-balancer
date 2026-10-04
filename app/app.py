import os
import socket

from flask import Flask, jsonify


def create_app():
    app = Flask(__name__)
    # Each container gets its own SERVER_NAME from docker-compose.yml
    server_name = os.environ.get("SERVER_NAME", socket.gethostname())

    @app.route("/")
    def home():
        return (
            f"<html><body style='font-family:sans-serif;text-align:center;margin-top:20vh'>"
            f"<h1>Served by: {server_name}</h1>"
            f"<p>Refresh the page to see the load balancer switch servers.</p>"
            f"</body></html>"
        )

    @app.route("/api/whoami")
    def whoami():
        return jsonify(server=server_name)

    @app.route("/health")
    def health():
        return jsonify(status="ok")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
