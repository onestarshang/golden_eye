$(function () {

    /*var ifcode = getParameterByName('ifcode'),
        period_short = getParameterByName('period_short'),
        period_long = getParameterByName('period_long'),
        date = getParameterByName('date');
    */
    var ifcode = $('#filter-ifcode').val(),
        periodshort = $('#filter-period_short').val(),
        periodlong = $('#filter-period_long').val();

    $.getJSON('/api/backtest/fitting_data?date=20151120&ifcode=if1511&period=400', function (data) {

        var price = data;

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
            }]
        });
    });
});
