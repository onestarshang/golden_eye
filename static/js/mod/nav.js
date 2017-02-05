(function() {
    function hrefToLevels(href) {
        href = href.split('?')[0];
        if (href.slice(-1) == '/') {
            return href.slice(0, -1);
        } else {
            return href;
        }
    }

    var urlLevels = hrefToLevels(location.pathname);

    $('.navbar-fixed-top .navbar-nav li a').each(function(i, n) {
        var hrefLevels = hrefToLevels($(n).attr('href'));
        if (urlLevels.lastIndexOf(hrefLevels, 0) === 0) {
            $(n).parent().addClass('active');
        }
    });

    $('.side-nav .list-group .list-group-item').each(function(i, n) {
        var hrefLevels = hrefToLevels($(n).attr('href'));
        if (urlLevels === hrefLevels) {
            $(n).addClass('active');
        }
    });
})();
