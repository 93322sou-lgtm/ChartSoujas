# ws_module.py
import websocket
import json
from threading import Thread

def ws_connect(tickers=[], ohlc=[], on_message=None, on_error=None, on_close=None):
    """
    Start websocket connection and subscribe to tickers and OHLC channels.
    tickers: list of symbols for v2/ticker
    ohlc: list of symbols for candlestick_1m
    on_message: callback(msg)
    on_error: callback(err)
    on_close: callback(code, msg)
    """
    WEBSOCKET_URL = "wss://socket.india.delta.exchange"

    def _on_message(ws, message):
        if on_message:
            on_message(json.loads(message))

    def _on_error(ws, error):
        if on_error:
            on_error(error)

    def _on_close(ws, close_status_code, close_msg):
        if on_close:
            on_close(close_status_code, close_msg)

    def _on_open(ws):
        print("📌 WebSocket opened")

        if tickers:
            payload = {
                "type": "subscribe",
                "payload": {"channels":[{"name":"v2/ticker","symbols":tickers}]}
            }
            ws.send(json.dumps(payload))

        if ohlc:
            payload = {
                "type": "subscribe",
                "payload": {"channels":[{"name":"candlestick_1m","symbols":ohlc}]}
            }
            ws.send(json.dumps(payload))

    ws_app = websocket.WebSocketApp(
        WEBSOCKET_URL,
        on_message=_on_message,
        on_error=_on_error,
        on_close=_on_close
    )
    ws_app.on_open = _on_open

    # Run in a separate thread so it doesn't block
    thread = Thread(target=ws_app.run_forever)
    thread.daemon = True
    thread.start()
    return ws_app


