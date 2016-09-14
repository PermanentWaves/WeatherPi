#!/usr/bin/python

from flask import Flask, render_template, abort
import bme280Get
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
bme280 = bme280Get.Bme280Get(db)

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

    temperature_hourly, pressure_hourly, humidity_hourly = bme280.get_hourly()
    data = {
        'temperature_hourly': temperature_hourly,
        'pressure_hourly': pressure_hourly,
        'humidity_hourly': humidity_hourly
    }
    return render_template(template, data=data)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
