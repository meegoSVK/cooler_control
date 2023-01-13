import temp_check
import memorydb
import time
import glob
import os
import configparser

cfg_parser = configparser.ConfigParser()
cfg_parser = ('confgig.txt')



sensor_path = '/sys/bus/w1/devices/'
rng = range(1,10)
list_of_sensors = glob.glob(sensor_path+'28*')

while True:
  for s in list_of_sensors:
    sns = temp_check.Sensor(os.path.basename(s))
    temp_store = memorydb.TemperatureStore(s)
    temperature, timestmp = sns.get_celsius()
    temp_store.add_value(temperature, timestmp)
    print(os.path.basename(s), ' ',temp_store.mean())
  time.sleep(5)
  print()
