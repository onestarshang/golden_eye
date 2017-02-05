Array.prototype.max = function() {
      return Math.max.apply(null, this);
};

Array.prototype.min = function() {
      return Math.min.apply(null, this);
};

function numberToDaysOfWeek(num) {
    var map = {0: '日', 1: '一', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六', 7: '日'}
    return '周' + map[num];
}

function numberWithCommas(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function fillupDateNum(num) {
    return num = num < 10 ? '0' + num : num;
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)'),
        results = regex.exec(location.search);
    return results == null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
}

function getMobileAppKey() {
    var regex = new RegExp('^/app/([0-9]+)/'),
        results = regex.exec(location.pathname);
    return results == null ? '' : results[1];
}

function getAppKeyRetentionEvent() {
    var regex = new RegExp('^/event_retention/([0-9]+)/'),
        results = regex.exec(location.pathname);
    return results == null ? '' : results[1];
}

function getProductKey() {
    var regex = new RegExp('^/piwik/([0-9]+)/'),
        results = regex.exec(location.pathname);
    return results == null ? '' : results[1];
}

function getProductKeyWebApp() {
    var regex = new RegExp('^/webapp/([0-9]+)/'),
        results = regex.exec(location.pathname);
    return results == null ? '' : results[1];
}

function getProductKeyMobileweb() {
    var regex = new RegExp('^/mobile_web/([0-9]+)/'),
        results = regex.exec(location.pathname);
    return results == null ? '' : results[1];
}

function getVirtualAppKey() {
    var name = location.pathname.split('/')[1];
    if (name === 'group') {
        return -11;  // refer to models.consts.VIRTUAL_APP_KEY
    }
    return '';
}

function dayAfter(n, day, format) {
    var format = format || "YYYYMMDD";
    var d = moment(day, format);
    return d.add('days', n).format(format);
}

var delay = (function() {
    var timer = 0;
    return function(callback, ms) {
        clearTimeout(timer);
        timer = setTimeout(callback, ms);
    }
})();

function substringMatcher (strs) {
    return function findMatches(q, cb) {
        var matches, substringRegex;

        // an array that will be populated with substring matches
        matches = [];

        // regex used to determine if a string contains the substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string that
        // contains the substring `q`, add it to the `matches` array
        $.each(strs, function(i, str) {
            if (substrRegex.test(str)) {
              // the typeahead jQuery plugin expects suggestions to a
              // JavaScript object, refer to typeahead docs for more info
              matches.push({ value: str });
            }
        });

        cb(matches);
    };
};
