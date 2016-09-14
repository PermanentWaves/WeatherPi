$(document).ready(function () {
    swiper();
    bme280_current();
    bme280_hourly();
});

function swiper() {
        Swiper ('.swiper-container', {
        direction: 'horizontal',
        loop: false,
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev'
    })
}

function bme280_current() {
    $("#bme280-current").load('/bme280-current')
    setTimeout('bme280_current()', 60000);
}

function bme280_hourly() {
    $("#bme280-temperature-hourly-slide").load('/bme280-hourly/temperature')
    $("#bme280-pressure-hourly-slide").load('/bme280-hourly/pressure')
    $("#bme280-humidity-hourly-slide").load('/bme280-hourly/humidity')
    setTimeout('bme280_hourly()', 360000);
}
