from datetime import datetime
class Sensor:

   def __init__(self, sensor_mac, sensor_path = '/sys/bus/w1/devices/'):
     self.sensor_path = sensor_path
     self.sensor_mac = sensor_mac

   def get_temperature(self):
     file_path = self.sensor_path + self.sensor_mac + '/w1_slave'
     f = open(file_path, 'r')
     rawtemp = int(f.readlines()[1].split('t=')[1].replace("\n",''))
     return rawtemp, datetime.now()

   def get_celsius(self):
     raw_temp, timestamp = self.get_temperature()
     return raw_temp / 1000, timestamp
