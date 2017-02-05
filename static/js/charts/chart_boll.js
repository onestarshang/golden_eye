$(function () {

    var ifcode = $('#filter-ifcode').val(),
        periodshort = $('#filter-period_short').val(),
        periodlong = $('#filter-period_long').val(),
        date = $('#date').val();

    $.getJSON('/api/realtime/boll/date/'+date+'/ifcode/'+ifcode+'/period_short/'+periodshort+'/period_long/'+periodlong, function (data) {

        var price = data[0],
            boll_up = data[1],
            boll_dn = data[2],
            boll_mb = data[3];


        // create the chart
        $('#container').highcharts('StockChart', {
            chart: {
                    zoomType: 'x',
                    width: 950
            },

            rangeSelector: {
                enabled: false
            },

            title: {
                text: ifcode
            },

            yAxis: {
                title: {
                    text: 'Price'
                }
            },

            series: [{
                type: 'line',
                name: 'Price',
                data: price,
                id: 'price_series'
            }, {
                type: 'line',
                name: 'boll_up',
                data: boll_up
            }, {
                type: 'line',
                name: 'boll_dn',
                data: boll_dn
            },
            {
                type: 'line',
                name: 'boll_mb',
                data: boll_mb
            }]
        });
    });
});
