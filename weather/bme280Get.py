from datetime import datetime, timedelta
import simplejson as json


class Bme280Get:

    def __init__(self, db):
        self.db = db

    def get_current(self):
        now = datetime.now()
        offset = now - timedelta(hours=2)
        c = self.db.cursor()
        query = "SELECT LOWER(DATE_FORMAT(date_time, '%%l:%%i %%p')) as date_time, " \
                "temperature, " \
                "pressure, " \
                "humidity " \
                "FROM bme280 " \
                "WHERE date_time > %s"
        c.execute(query, offset)
        data = c.fetchall()
        row = data[len(data) - 2]  # most recent row
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

    def get_hourly(self):
        c = self.db.cursor()
        offset = datetime.now() - timedelta(hours=48)
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
        return temperature, pressure, humidity

    def chart_sort(self, data):
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