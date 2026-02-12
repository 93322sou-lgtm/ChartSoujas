from flask import Flask, render_template, jsonify
import json
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/candles")
def candles():
    json_path = os.path.join(app.root_path, "candles.json")
    
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
