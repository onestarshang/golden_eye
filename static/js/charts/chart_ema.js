$(function () {

    var ifcode = $('#filter-ifcode').val(),
        periodshort = $('#filter-period_short').val(),
        periodlong = $('#filter-period_long').val(),
        date = $('#date').val();

    $.getJSON('/api/backtest/ema/date/'+date+'/ifcode/'+ifcode+'/period_short/'+periodshort+'/period_long/'+periodlong, function (data) {

        var price = data[0],
            ema_short = data[1],
            ema_long = data[2];


        // create the chart
        $('#container').highcharts('StockChart', {

            rangeSelector: {
                enabled: false
            },

            title: {
                text: ifcode
            },

            yAxis: [{
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Price'
                },
                height: '60%',
                lineWidth: 0.1
            }],

            series: [{
                type: 'line',
                name: 'Price',
                data: price,
                id: 'price_series'
            }, {
                type: 'line',
                name: 'ema_short',
                data: ema_short
            }, {
                type: 'line',
                name: 'ema_long',
                data: ema_long
            }]
        });
    });
});
