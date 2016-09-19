import sys
import os

sys.path.insert (0,'/home/pi/WeatherPi/weather')
os.chdir("/home/pi/WeatherPi/weather")

from weather import app as application
