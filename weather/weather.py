#!/usr/bin/python

from flask import Flask, render_template, abort
import bme280 as bme280db
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

app = Flask(__name__, static_url_path="", static_folder='web')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/bme280-current')
def bme280_current():
    temperature_current, pressure_current, humidity_current, current = bme280.get_current()
    data = {
        'current': current,
        'temperature_current': temperature_current,
        'pressure_current': pressure_current,
        'humidity_current': humidity_current
    }
    return render_template('bme280_current.html', data=data)


@app.route('/bme280-hourly/<template>')
def bme280_hourly(template):
    templates = {
        'temperature': 'bme280_temperature_hourly.html',
        'pressure': 'bme280_pressure_hourly.html',
        'humidity': 'bme280_humidity_hourly.html'
    }
    try:
        template = templates[template]
    except KeyError:
        abort(404)

    temperature_hourly, pressure_hourly, humidity_hourly = bme280.get_hourly_average()
    data = {
        'temperature_hourly': temperature_hourly,
        'pressure_hourly': pressure_hourly,
        'humidity_hourly': humidity_hourly
    }
    return render_template(template, data=data)


@app.route('/bme280-weekly/<template>')
def bme280_weekly(template):
    templates = {
        'temperature': 'bme280_temperature_weekly.html',
        'pressure': 'bme280_pressure_weekly.html',
        'humidity': 'bme280_humidity_weekly.html'
    }
    try:
        template = templates[template]
    except KeyError:
        abort(404)

    temperature_weekly, pressure_weekly, humidity_weekly = bme280.get_weekly()
    data = {
        'temperature_weekly': temperature_weekly,
        'pressure_weekly': pressure_weekly,
        'humidity_weekly': humidity_weekly
    }
    return render_template(template, data=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
