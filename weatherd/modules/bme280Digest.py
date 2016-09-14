from datetime import datetime


class Bme280Digest:
    def __init__(self, db, scheduler, interval):
        self.timer = None
        self.db = db
        self.scheduler = scheduler
        self.interval = interval
        print 'Bme280Digest is alive!'

    def start(self):
        c = self.db.cursor()
        try:
            today = "{:%Y-%m-%d}".format(datetime.today())
            # Hourly digest
            query = "INSERT INTO bme280_hourly " \
                    "(date_time, " \
                    "temperature_high, temperature_low, " \
                    "pressure_high, pressure_low, " \
                    "humidity_high, humidity_low) " \
                    "SELECT " \
                    "DATE_FORMAT(date_time, '%Y-%m-%d %H:00:00') AS dt, " \
                    "MAX(temperature) AS temperature_high, MIN(temperature) AS temperature_low, " \
                    "MAX(pressure) AS pressure_high, MIN(pressure) AS pressure_low, " \
                    "MAX(humidity) AS humidity_high, MIN(humidity) AS humidity_low " \
                    "FROM bme280 " \
                    "WHERE bme280.date_time < '" + today + "' " \
                    "GROUP BY dt "

            c.execute(query)
            # Daily digest
            query = "INSERT INTO bme280_daily " \
                    "(date_time, " \
                    "temperature_high, temperature_low, " \
                    "pressure_high, pressure_low, " \
                    "humidity_high, humidity_low)" \
                    "SELECT " \
                    "DATE_FORMAT(bme280.date_time, '%Y-%m-%d 01:00:00') AS dt, " \
                    "MAX(temperature), MIN(temperature), " \
                    "MAX(pressure), MIN(pressure), " \
                    "MAX(humidity), MIN(humidity) " \
                    "FROM bme280 " \
                    "WHERE bme280.date_time < '" + today + "' " \
                    "GROUP BY dt"
            c.execute(query)
            # Remove previous day's minute data
            # query = "DELETE FROM bme280 WHERE date_time < %s"
            # c.execute(query, today)
        except Exception:
            raise
        self.db.commit()
        c.close()
        self.timer = self.scheduler.enter(self.interval, 10, self.start, [])

    def stop(self):
        print 'Bme280Daily stopping...'
        if self.timer:
            self.scheduler.cancel(self.timer)
