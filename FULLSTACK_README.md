# Full-Stack Real-Time Chart Application

## Architecture
- **Backend**: Flask + Flask-SocketIO + WebSocket (Delta Exchange)
- **Frontend**: React + TradingView Lightweight Charts + Socket.IO Client

## Setup & Run

### 1. Start Backend Server
```bash
cd /workspaces/ChartSoujas/Poject_Algo
python server.py
```
Backend runs on: http://localhost:5000

### 2. Start React Frontend
```bash
cd /workspaces/ChartSoujas/ReactCreateChart/my-app
npm start
```
Frontend runs on: http://localhost:3000

## Features
- ✅ Loads historical candle data from candles.json
- ✅ Real-time WebSocket updates from Delta Exchange
- ✅ Auto-updates candles.json with new data
- ✅ Live chart updates via Socket.IO
- ✅ Fullscreen responsive chart
- ✅ Proper time scale formatting

## API Endpoints
- GET /candles - Returns sorted historical candle data

## WebSocket Events
- new_candle - Emitted when new candle data arrives
