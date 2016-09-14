import sys
import os

sys.path.insert (0,'/home/pi/Weather/weather')
os.chdir("/home/pi/Weather/weather")

from weather import app as application
