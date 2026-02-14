from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import json
import os
from ws_module import ws_connect

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

CANDLES_FILE = os.path.join(app.root_path, "candles.json")

@app.route("/")
def index():
    return jsonify({"status": "running"})

@app.route("/candles")
def get_candles():
    try:
        with open(CANDLES_FILE, "r") as f:
            data = json.load(f)
        sorted_data = sorted(data, key=lambda x: x['time'])
        return jsonify(sorted_data)
    except FileNotFoundError:
        return jsonify({"error": "Data file not found"}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON format"}), 500

def handle_ws_message(msg):
    """Handle WebSocket messages from Delta Exchange"""
    if msg.get('type') == 'candlestick_1m':
        candle_data = msg.get('candle', {})
        new_candle = {
            "time": candle_data.get('time'),
            "open": candle_data.get('open'),
            "high": candle_data.get('high'),
            "low": candle_data.get('low'),
            "close": candle_data.get('close'),
            "volume": candle_data.get('volume')
        }
        
        # Update candles.json
        try:
            with open(CANDLES_FILE, "r") as f:
                candles = json.load(f)
            candles.append(new_candle)
            with open(CANDLES_FILE, "w") as f:
                json.dump(candles, f)
        except:
            pass
        
        # Emit to connected clients
        socketio.emit('new_candle', new_candle)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == "__main__":
    # Start WebSocket connection to Delta Exchange
    ws_connect(
        ohlc=["BTCUSD"],
        on_message=handle_ws_message
    )
    
    print("\n🚀 Server starting on http://localhost:5000")
    print("📊 WebSocket connected to Delta Exchange")
    print("✅ Ready to serve candle data\n")
    
    socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
