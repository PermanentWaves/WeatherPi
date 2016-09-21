#!/usr/bin/python

from flask import Flask, render_template, abort, request
import bme280 as bme280db
import menu as site_menu
import db as persist
import sys
import logging

logging.basicConfig(stream=sys.stderr)

db_info = {
    'host': 'localhost',
    'database': 'weather',
    'username': 'root',
    'password': 'root'
}

db = persist.Db(db_info)
bme280 = bme280db.Bme280(db)
menu = site_menu.Menu()

app = Flask(__name__, static_url_path="", static_folder='web')


@app.route('/')
def bme280_current():
    try:
        int(request.args.get('range'))
    except (NameError, TypeError):
        hours = 2
    else:
        hours = int(request.args.get('range'))

    if hours < 1:
        hours = 2
    temperature_current, pressure_current, humidity_current, current = bme280.get_current(hours)
    data = {
        'menu': menu.get('/'),
        'current': current,
        'temperature_current': temperature_current,
        'pressure_current': pressure_current,
        'humidity_current': humidity_current
    }
    return render_template('current.html', data=data)


@app.route('/bme280-averaged/<sensor>')
def bme280_averaged(sensor):
    try:
        int(request.args.get('range'))
    except (NameError, TypeError):
        hours = 48
    else:
        hours = int(request.args.get('range'))

    if hours < 1:
        hours = 48

    data = {'menu': menu.get('/bme280-averaged/' + sensor)}
    templates = {
        'temperature': {'icon': 'wi wi-thermometer blue', 'title': 'Temperature Averaged Last %s hours' % hours},
        'pressure': {'icon': 'wi wi-barometer yellow', 'title': 'Pressure Averaged Last %s hours' % hours},
        'humidity': {'icon': 'wi wi-humidity green', 'title': 'Humidity Averaged Last %s hours' % hours}
    }
    try:
        data.update(templates[sensor])
    except KeyError:
        abort(404)

    averaged = bme280.get_averaged(hours)
    data.update({'chart': averaged[sensor]})

    return render_template('chart.html', data=data)


@app.route('/bme280-high-low/<sensor>')
def bme280_high_low(sensor):
    try:
        int(request.args.get('range'))
    except (NameError, TypeError):
        days = 14
    else:
        days = int(request.args.get('range'))

    if days < 1:
        days = 14

    data = {'menu': menu.get('/bme280-high-low/' + sensor)}
    templates = {
        'temperature': {'icon': 'wi wi-thermometer blue', 'title': 'Temperature High/Low Last %s days' % days},
        'pressure': {'icon': 'wi wi-barometer yellow', 'title': 'Pressure High/Low Last %s days' % days},
        'humidity': {'icon': 'wi wi-humidity green', 'title': 'Humidity High/Low Last %s days' % days}
    }
    try:
        data.update(templates[sensor])
    except KeyError:
        abort(404)

    high_low = bme280.get_high_low(days)
    data.update({'chart': high_low[sensor]})
    return render_template('chart.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
