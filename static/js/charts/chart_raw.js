$(function () {

    var ifcode = $('#filter-ifcode').val(),
        date = $('#date').val();

    $.getJSON('/api/backtest/raw_data/date/'+date+'/ifcode/'+ifcode, function (data) {

        var price = data[0],
            volume = data[1];


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
            },
            {
                labels: {
                    align: 'right',
                    x: -3
                },
                title: {
                    text: 'Volume'
                },
                top: '65%',
                height: '35%',
                offset: 0,
                lineWidth: 2
            }],

            series: [{
                type: 'line',
                name: 'Price',
                data: price,
                id: 'price_series'
            }, {
                type: 'column',
                name: 'Volume',
                data: volume,
                yAxis: 1
            }]
        });
    });
});
