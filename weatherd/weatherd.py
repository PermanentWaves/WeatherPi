#!/usr/bin/python

import sched
import sys
import time
import db


class WeatherD:

    MINUTE = 60
    HOUR = 3600
    DAY = 86400

    # Config Start
    active_modules = {
        'bme280': True,
        'bme280Digest': False,
    }
    bme280_interval = MINUTE
    bme280Digest_interval = HOUR * 6
    db_info = {
        'host': 'localhost',
        'database': 'weather',
        'username': 'root',
        'password': 'root'
    }
    # Config Stop

    def __init__(self):
        self.modules = {}
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.db = db.Db(self.db_info)
        if self.active_modules['bme280']:
            from modules import bme280
            try:
                self.modules['bme280'] = bme280.Bme280(self.db, self.scheduler, self.bme280_interval)
            except ValueError as error:
                print error.message
                del self.active_modules['bme280']
            except IOError:
                print 'UNABLE TO LOAD BME280!'
                del self.active_modules['bme280']
        if self.active_modules['bme280Digest']:
            from modules import bme280Digest
            self.modules['bme280Digest'] = bme280Digest.Bme280Digest(self.db, self.scheduler, self.bme280Digest_interval)

    def start(self):
        for module, state in self.active_modules.iteritems():
            if state:
                start = getattr(self.modules[module], 'start')
                if callable(start):
                    start()
        self.scheduler.run()

    def stop(self):
        if self.db.con:
            self.db.close()
        for module, state in self.active_modules.iteritems():
            if state:
                stop = getattr(self.modules[module], 'stop')
                if callable(stop):
                    stop()
        sys.exit()


if __name__ == '__main__':
    weather = WeatherD()
    try:
        weather.start()
        while 1:
            pass
    except (KeyboardInterrupt, SystemExit):
        weather.stop()
