$(function () {

    var ifcode = $('#filter-ifcode').val(),
        periodshort = $('#filter-period_short').val(),
        periodlong = $('#filter-period_long').val(),
        display_num = $('#filter-display_num').val();

    var url = '/api/backtest/dates/ifcode/' + ifcode + '/display_num/' + display_num

    $.getJSON(url,function(result){
        $.each(result.date_list, function(i, date){
            $("div#container").append('<div id="container_'+date+'" class="col-md-6"></div>');
            $.getJSON('/api/backtest/macd/date/'+date+'/ifcode/'+ifcode+'/period_short/'+periodshort+'/period_long/'+periodlong, function (data) {

                var price = data[0],
                    macd_short = data[1],
                    macd_long = data[2],
                    out_flags = data[3];

                // create the chart
                $('#container_'+date).highcharts('StockChart', {
                    chart: {
                        zoomType: 'x',
                        width: 480
                    },

                    rangeSelector: {
                        enabled: false
                    },

                    title: {
                        text: ifcode + '_' + date
                    },

                    yAxis: [{
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'Price'
                        },
                        height: '70%',
                        lineWidth: 0.1
                    }, {
                        labels: {
                            align: 'right',
                            x: -3
                        },
                        title: {
                            text: 'MACD'
                        },
                        top: '65%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 0.1
                    }],

                    series: [{
                        type: 'line',
                        name: 'macd_short',
                        data: macd_short,
                        yAxis: 1
                    }, {
                        type: 'line',
                        name: 'macd_long',
                        data: macd_long,
                        yAxis: 1
                    }, {
                        type: 'line',
                        name: 'price',
                        data: price,
                        id: 'price_series'
                    }, {
                        type: 'flags',
                        data: (function(){
                            var flags = [],
                                dataLength = out_flags.length,
                                i = 0;
                            for (i; i < dataLength; i += 1) {
                                flags.push({
                                            x: out_flags[i][0],
                                            title: out_flags[i][1],
                                            text: out_flags[i][1] + ":" + out_flags[i][2]
                                }
                                );
                            }
                            return flags;
                        }()),
                        onSeries: 'price_series',
                        shape: 'circlepin',
                        width: 16
                       }]
                });
            });
        });
    });
});
