$(document).ready(function () {
    swiper();
    update_minutely();
    update_hourly();
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

function update_minutely() {
    $("#bme280-current").load('/bme280-current');
    setTimeout('update_minutely()', 60000);
}

function update_hourly() {
    $("#bme280-temperature-hourly-slide").load('/bme280-hourly/temperature');
    $("#bme280-pressure-hourly-slide").load('/bme280-hourly/pressure');
    $("#bme280-humidity-hourly-slide").load('/bme280-hourly/humidity');
    $("#bme280-temperature-weekly-slide").load('/bme280-weekly/temperature');
    $("#bme280-pressure-weekly-slide").load('/bme280-weekly/pressure');
    $("#bme280-humidity-weekly-slide").load('/bme280-weekly/humidity');
    setTimeout('update_hourly()', 360000);
}
