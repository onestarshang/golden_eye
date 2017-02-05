(function() {
    $('.datepicker').datepicker({format: 'yyyy-mm-dd'});
    $('#begin_date').datepicker().on('show', function(ev) {
        $('#end_date').datepicker('hide');
    });
    $('#end_date').datepicker().on('show', function(ev) {
        $('#begin_date').datepicker('hide');
    });

    $('.refresh').on('click', function() {
        var beginDate = $('#begin_date').length > 0 && moment($('#begin_date').val()).format('YYYYMMDD')
                                                    || moment($('#date').val()).format('YYYYMMDD'),
            endDate = $('#end_date').length > 0 && moment($('#end_date').val()).format('YYYYMMDD')
                                                || moment($('#date').val()).format('YYYYMMDD'),
            theDate = $('#date').length > 0 && moment($('#date').val()).format('YYYYMMDD')
                                                || moment($('#date').val()).format('YYYYMMDD'),
            ifcode = $('#filter-ifcode').val(),
            periodshort = $('#filter-period_short').val(),
            periodlong = $('#filter-period_long').val(),
            displaynum = $('#filter-display_num').val(),
            transamount = $('#filter-trans_amount').val();

        var href = location.href,
            ptheDate = getParameterByName('date'),
            pBeginDate = getParameterByName('begin_date'),
            pEndDate = getParameterByName('end_date'),
            pIfcode = getParameterByName('ifcode'),
            pPeriodshort = getParameterByName('period_short'),
            pPeriodlong = getParameterByName('period_long'),
            pDisplaynum = getParameterByName('display_num'),
            pTransamount = getParameterByName('trans_amount');

        function updateHref(href, argName, newValue, oldValue) {
            argName += '=';
            if (!newValue || newValue === undefined || newValue === 'undefined') {
                if (href.search('&' + argName) > 0) {
                    href = href.replace('&' + argName + oldValue, '');
                } else if (href.search(argName) > 0) {
                    href = href.replace(argName + oldValue, '');
                }
                return href;
            } else {
                if (href.search(argName) > 0) {
                    href = href.replace(argName + encodeURI(oldValue), argName + newValue);
                } else {
                    href = href + '&' + argName + newValue
                }
            }
            return href;
        }
        href = updateHref(href, 'date', theDate, ptheDate);
        href = updateHref(href, 'ifcode', ifcode, pIfcode);
        href = updateHref(href, 'period_short', periodshort, pPeriodshort);
        href = updateHref(href, 'period_long', periodlong, pPeriodlong);
        href = updateHref(href, 'display_num', displaynum, pDisplaynum);
        href = updateHref(href, 'trans_amount', transamount, pTransamount);

        location.href = href;
    });
})();
