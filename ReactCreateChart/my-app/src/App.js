import React, {useRef, useEffect} from 'react'
import { createChart } from 'lightweight-charts';
import io from 'socket.io-client';

function App() {
  const chartcontainerRef = useRef()
  const chartRef = useRef()
  const seriesRef = useRef()

  useEffect(() => {
    const chartOptions = { 
      layout: { 
        textColor: 'white', 
        background: { type: 'solid', color: 'black' } 
      },
      width: window.innerWidth,
      height: window.innerHeight,
      timeScale: {
        timeVisible: true,
        secondsVisible: false,
      }
    };
    
    const chart = createChart(chartcontainerRef.current, chartOptions);
    chartRef.current = chart;
    
    const candlestickSeries = chart.addCandlestickSeries({ 
      upColor: '#26a69a', 
      downColor: '#ef5350', 
      borderVisible: false, 
      wickUpColor: '#26a69a', 
      wickDownColor: '#ef5350' 
    });
    seriesRef.current = candlestickSeries;

    // Fetch historical data
    fetch('http://localhost:5000/candles')
      .then(r => r.json())
      .then(data => {
        const formattedData = data.map(d => ({
          open: d.open,
          high: d.high,
          low: d.low,
          close: d.close,
          time: d.time
        }));
        candlestickSeries.setData(formattedData);
        chart.timeScale().fitContent();
      })

    // Connect to WebSocket for real-time updates
    const socket = io('http://localhost:5000');
    
    socket.on('connect', () => {
      console.log('Connected to server');
    });

    socket.on('new_candle', (candle) => {
      candlestickSeries.update({
        time: candle.time,
        open: candle.open,
        high: candle.high,
        low: candle.low,
        close: candle.close
      });
    });

    const handleResize = () => {
      chart.applyOptions({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    
    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      socket.disconnect();
      chart.remove();
    }
  }, [])

  return <div ref={chartcontainerRef} />
}

export default App;
