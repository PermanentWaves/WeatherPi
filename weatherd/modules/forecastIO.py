
import time
import os


class ForecastIO:

    base_url = 'https://api.forecast.io/forecast/'
    parameters = '?exclude=minutely,hourly,flags'

    def __init__(self, db, scheduler, interval, latitude, longitude):
        self.timer = None
        self.db = db
        self.scheduler = scheduler
        self.interval = interval
        # latitude, longitude in decimal
        location = "/" + latitude + "," + longitude + "/"
        self.api_url = self.base_url + os.environ['FORECAST_IO_API'] + location + self.parameters
        print 'ForecastIO is alive!'

    def start(self):
        old = time.time() - self.interval
        self.timer = self.scheduler.enter(self.interval, 10, self.start, [])

    def stop(self):
        print 'ForecastIO stopping...'
        if self.timer:
            self.scheduler.cancel(self.timer)
