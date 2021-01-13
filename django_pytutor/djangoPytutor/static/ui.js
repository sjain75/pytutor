$(window).on('load', function () {
    $(window).on('scroll', function() {
        if ($(window).scrollTop() > 10) {
            $('.navbar').addClass('nav-active');
        } else {
            $('.navbar').removeClass('nav-active');
        }
    })
})