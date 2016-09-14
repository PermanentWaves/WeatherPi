from Adafruit_BME280 import *


class Bme280:

    def __init__(self, db, scheduler, interval):
        self.timer = None
        self.db = db
        self.scheduler = scheduler
        self.interval = interval
        try:
            self.sensor = BME280(mode=BME280_OSAMPLE_8)
            print 'Bme280 is alive!'
        except ValueError:
            raise

    def start(self):
        temperature = self.sensor.read_temperature()
        temperature = temperature * 1.8 + 32
        pascals = self.sensor.read_pressure()
        pressure = pascals / 100
        humidity = self.sensor.read_humidity()
        c = self.db.cursor()
        query = "INSERT INTO bme280 (date_time, temperature, pressure, humidity) " \
                "VALUES (NOW(), '%s', '%s', '%s')"
        c.execute(query, (temperature, pressure, humidity))
        self.db.commit()
        c.close()
        self.timer = self.scheduler.enter(self.interval, 1, self.start, [])

    def stop(self):
        print 'Bme280 stopping...'
        if self.timer:
            self.scheduler.cancel(self.timer)
