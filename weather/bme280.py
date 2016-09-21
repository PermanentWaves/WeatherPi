from datetime import datetime, timedelta
import simplejson as json


class Bme280:

    def __init__(self, db):
        self.db = db

    def get_current(self, span):
        now = datetime.now()
        offset = now - timedelta(hours=span)
        c = self.db.cursor()
        query = "SELECT LOWER(DATE_FORMAT(date_time, '%%l:%%i %%p')) as date_time, " \
                "temperature, " \
                "pressure, " \
                "humidity " \
                "FROM bme280 " \
                "WHERE date_time > %s"
        c.execute(query, offset)
        data = c.fetchall()
        row = data[len(data) - span]  # most recent row
        current_label = "{:%l:%M %p}".format(offset) + " - " + "{:%l:%M %p}".format(now)
        current_label = current_label.lower()
        current = {
            'label': current_label,
            'temperature': ('%.2f' % row[1]).rstrip('0').rstrip('.'),
            'pressure': ('%.4f' % row[2]).rstrip('0').rstrip('.'),
            'humidity': ('%.2f' % row[3]).rstrip('0').rstrip('.')
        }
        (labels, temperature, pressure, humidity) = self.chart_sort(data)
        temperature = self.chart_data(labels, 'Temperature', '#1ca8dd', temperature)
        pressure = self.chart_data(labels, 'Pressure', '#e4d836', pressure)
        humidity = self.chart_data(labels, 'Humidity', '#1bc98e', humidity)
        c.close()
        return temperature, pressure, humidity, current

    def get_averaged(self, span):
        c = self.db.cursor()
        offset = datetime.now() - timedelta(hours=span)
        query = "SELECT LOWER(DATE_FORMAT(date_time, '%%D %%l:00 %%p')) AS dt, " \
                "AVG(temperature) AS temperature, " \
                "AVG(pressure) AS pressure, " \
                "AVG(humidity) AS humidity " \
                "FROM bme280 " \
                "WHERE bme280.date_time > %s " \
                "GROUP BY dt " \
                "ORDER BY date_time"
        c.execute(query, offset)
        (labels, temperature, pressure, humidity) = self.chart_sort(c.fetchall())
        temperature = self.chart_data(labels, 'Temperature', '#1ca8dd', temperature)
        pressure = self.chart_data(labels, 'Pressure', '#e4d836', pressure)
        humidity = self.chart_data(labels, 'Humidity', '#1bc98e', humidity)
        return {'temperature': temperature, 'pressure': pressure, 'humidity': humidity}

    def get_high_low(self, span):
        c = self.db.cursor()
        offset = datetime.now() - timedelta(hours=(span * 24))
        query = "SELECT DATE_FORMAT(date_time, '%%b %%D') AS dt, " \
                "MAX(temperature) AS temperature_high, " \
                "MIN(temperature) AS temperature_low, " \
                "MAX(pressure) AS pressure_high, " \
                "MIN(pressure) AS pressure_low, " \
                "MAX(humidity) AS humidity_high, " \
                "MIN(humidity) AS humidity_low " \
                "FROM bme280 " \
                "WHERE bme280.date_time > %s " \
                "GROUP BY dt " \
                "ORDER BY date_time"
        c.execute(query, offset)
        (labels, temperature_high, temperature_low, pressure_high, pressure_low, humidity_high, humidity_low) = \
            self.chart_sort_high_low(c.fetchall())
        temperature = self.chart_data_high_low(labels, '#1ca8dd', '#656565', temperature_high, temperature_low)
        pressure = self.chart_data_high_low(labels, '#e4d836', '#656565', pressure_high, pressure_low)
        humidity = self.chart_data_high_low(labels, '#1bc98e', '#656565', humidity_high, humidity_low)
        return {'temperature': temperature, 'pressure': pressure, 'humidity': humidity}

    @staticmethod
    def chart_sort(data):
        labels = []
        temperature = []
        pressure = []
        humidity = []
        for event in data:
            labels.append(event[0])
            temperature.append(('%.2f' % event[1]).rstrip('0').rstrip('.'))
            pressure.append(('%.4f' % event[2]).rstrip('0').rstrip('.'))
            humidity.append(('%.2f' % event[3]).rstrip('0').rstrip('.'))
        return labels, temperature, pressure, humidity

    @staticmethod
    def chart_data(labels, label, color, data):
        cdata = {
            'labels': labels,
            'datasets': [
                {
                    'label': label,
                    'fill': False,
                    'lineTension': .5,
                    'backgroundColor': "#434857",
                    'borderColor': color,
                    'borderCapStyle': 'butt',
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'borderJoinStyle': 'miter',
                    'pointBorderColor': color,
                    'pointBackgroundColor': "#fff",
                    'pointBorderWidth': 1,
                    'pointHoverRadius': 5,
                    'pointHoverBackgroundColor': color,
                    'pointHoverBorderColor': "#1ca8dd",
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 1,
                    'pointHitRadius': 10,
                    'data': data,
                    'spanGaps': False,
                }
            ]
        }
        return json.dumps(cdata)

    @staticmethod
    def chart_sort_high_low(data):
        labels = []
        temperature_high = []
        temperature_low = []
        pressure_high = []
        pressure_low = []
        humidity_high = []
        humidity_low = []
        for event in data:
            labels.append(event[0])
            temperature_high.append(('%.2f' % event[1]).rstrip('0').rstrip('.'))
            temperature_low.append(('%.2f' % event[2]).rstrip('0').rstrip('.'))
            pressure_high.append(('%.4f' % event[3]).rstrip('0').rstrip('.'))
            pressure_low.append(('%.4f' % event[4]).rstrip('0').rstrip('.'))
            humidity_high.append(('%.2f' % event[5]).rstrip('0').rstrip('.'))
            humidity_low.append(('%.2f' % event[6]).rstrip('0').rstrip('.'))
        return labels, temperature_high, temperature_low, pressure_high, pressure_low, humidity_high, humidity_low

    @staticmethod
    def chart_data_high_low(labels, color_high, color_low, high, low):
        cdata = {
            'labels': labels,
            'datasets': [
                {
                    'label': 'High',
                    'fill': False,
                    'lineTension': .5,
                    'backgroundColor': "#434857",
                    'borderColor': color_high,
                    'borderCapStyle': 'butt',
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'borderJoinStyle': 'miter',
                    'pointBorderColor': color_high,
                    'pointBackgroundColor': "#fff",
                    'pointBorderWidth': 1,
                    'pointHoverRadius': 5,
                    'pointHoverBackgroundColor': color_high,
                    'pointHoverBorderColor': "#1ca8dd",
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 1,
                    'pointHitRadius': 10,
                    'data': high,
                    'spanGaps': False,
                },
                {
                    'label': 'Low',
                    'fill': False,
                    'lineTension': .5,
                    'backgroundColor': "#434857",
                    'borderColor': color_low,
                    'borderCapStyle': 'butt',
                    'borderDash': [],
                    'borderDashOffset': 0.0,
                    'borderJoinStyle': 'miter',
                    'pointBorderColor': color_low,
                    'pointBackgroundColor': "#fff",
                    'pointBorderWidth': 1,
                    'pointHoverRadius': 5,
                    'pointHoverBackgroundColor': color_low,
                    'pointHoverBorderColor': "#1ca8dd",
                    'pointHoverBorderWidth': 2,
                    'pointRadius': 1,
                    'pointHitRadius': 10,
                    'data': low,
                    'spanGaps': False,
                }
            ]
        }
        return json.dumps(cdata)
