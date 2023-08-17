from flask import Flask, render_template
import os

PORT = 9090
HOST = "0.0.0.0"

app = Flask(__name__)


@app.route('/')
def home():
    return "hello flask!", 200


if __name__ == "__main__":
    print(f"Running on http://{HOST}:{PORT}")
    app.run(debug=True, host=HOST, port=PORT)
