const chart = LightweightCharts.createChart(
    document.getElementById('container'),
    {
        layout: {
            textColor: 'white',
            background: { type: 'solid', color: 'black' }
        },
        grid: {
            vertLines: { color: '#222' },
            horzLines: { color: '#222' }
        }
    }
);

const candleSeries = chart.addSeries(
    LightweightCharts.CandlestickSeries,
    {
        upColor: '#26a69a',
        downColor: '#ef5350',
        borderVisible: false,
        wickUpColor: '#26a69a',
        wickDownColor: '#ef5350'
    }
);

// fetch data from Flask
fetch('/candles')
    .then(r => r.json())
    .then(data => {

        // if your python sends ms timestamps, fix here
        for (const c of data) {
            if (c.time > 10_000_000_000) {
                c.time = Math.floor(c.time / 1000);
            }
        }

        candleSeries.setData(data);
        chart.timeScale().fitContent();
    })
    .catch(err => console.error(err));


// resize handling
window.addEventListener('resize', () => {
    chart.applyOptions({
        width: document.getElementById('container').clientWidth,
        height: document.getElementById('container').clientHeight
    });
});
