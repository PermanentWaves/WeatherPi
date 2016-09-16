#!/usr/bin/python

from flask import Flask, render_template, abort
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
    temperature_current, pressure_current, humidity_current, current = bme280.get_current()
    data = {
        'menu': menu.get('/'),
        'current': current,
        'temperature_current': temperature_current,
        'pressure_current': pressure_current,
        'humidity_current': humidity_current
    }
    return render_template('current.html', data=data)


@app.route('/bme280-hourly/<template>')
def bme280_hourly(template):
    data = {'menu': menu.get('/bme280-hourly/' + template)}
    templates = {
        'temperature': {'icon': 'wi wi-thermometer blue', 'title': '48hr Averaged Temperature'},
        'pressure': {'icon': 'wi wi-barometer yellow', 'title': '48hr Averaged Pressure'},
        'humidity': {'icon': 'wi wi-humidity green', 'title': '48hr Averaged Humidity'}
    }
    try:
        data.update(templates[template])
    except KeyError:
        abort(404)

    hourly = bme280.get_hourly_average()
    data.update({'chart': hourly[template]})

    return render_template('chart.html', data=data)


@app.route('/bme280-weekly/<template>')
def bme280_weekly(template):
    data = {'menu': menu.get('/bme280-weekly/' + template)}
    templates = {
        'temperature': {'icon': 'wi wi-thermometer blue', 'title': '2 Weeks Temperature'},
        'pressure': {'icon': 'wi wi-barometer yellow', 'title': '2 Weeks Pressure'},
        'humidity': {'icon': 'wi wi-humidity green', 'title': '2 Weeks Humidity'}
    }
    try:
        data.update(templates[template])
    except KeyError:
        abort(404)

    weekly = bme280.get_weekly()
    data.update({'chart': weekly[template]})
    return render_template('chart.html', data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
