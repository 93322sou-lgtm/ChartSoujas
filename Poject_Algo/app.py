from flask import Flask, render_template, jsonify
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/candles")
def candles():
    json_path = os.path.join(BASE_DIR, "static", "candles.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
