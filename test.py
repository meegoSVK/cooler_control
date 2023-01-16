import temp_check
import memorydb
import time
import glob
import os
import pigpio
import configparser
from checker import Checker

cfg_file_path = 'config.txt'

print(f'Reading configuration file {cfg_file_path}')
cfg_parser = configparser.ConfigParser()
cfg_parser.read(cfg_file_path)

parameters = {
  'SENSOR': {
    'sensor_id': {'type': 'str', 'default_value': None, 'mandatory': True},
  },
  'TEMPERATURE': {
    'interval': {'type': 'int', 'default_value': 60, 'mandatory': False},
    'retention': {'type': 'int', 'default_value': 5, 'mandatory': False},
    'limit_temperature': {'type': 'float', 'default_value': 0, 'mandatory': True},
    },
  'FAN': {
    'gpio_pin': {'type': 'int', 'default_value': 17, 'mandatory': False},
  },
}

def param_check(group, key, def_value, var_type, mandatory):
  name = f'[{group}][{key}]'
  try:
    opt_var = Checker(var_type, cfg_parser[group][key]).do_check()
  except ValueError:
    print(f'''
      Value of key {name} has different data type than expected.
      Expected data type is {var_type}.
      ''')
    if mandatory is True:
      print(f'Key {name} is mandatory. Please fix it and rerun program')
      exit(1)
    else:
      print(f'Key {name} is optional, setting value to default ({def_value})')
      opt_var = def_value
  except KeyError:
    print(f'Key {name} not present in config file')
    if mandatory is True:
      print(f'Key {name} is mandatory. Please fix it and rerun program')
      exit(1)
    else:
      print(f'Key {name} is optional, setting value to default ({def_value})')
      opt_var = def_value
  finally:
    return opt_var 
  
    
for param_group, param_list in parameters.items():
  for param_name, param_properties in param_list.items():
    globals()[param_name] = param_check(param_group, param_name, param_properties['default_value'], param_properties['type'], param_properties['mandatory'])

print()
print(
  f"""Configuration parsed. Using:
  Sensor: {sensor_id}
  Number of measurements: {retention}
  Interval between measurements: {interval}
  Limit temperature: {limit_temperature}
  """)

def fanCheck(current_temp):
  if current_temp >= limit_temperature and fan.read(gpio_pin) == 0:
    print(f'Zapinam PIN {gpio_pin} pretoze aktualny primere teplot ({current_temp}) je vacsi ako limit {limit_temperature}. FAN aktualne NEbezi')
    fan.write(gpio_pin, 1)
    return
  elif current_temp >= limit_temperature and fan.read(gpio_pin) == 1:
    print(f'NEMENIM PIN {gpio_pin} pretoze aktualny primere teplot ({current_temp}) je vacsi ako limit {limit_temperature} a FAN bezi')
    return
  elif current_temp < limit_temperature and fan.read(gpio_pin) == 1:
    print(f'Vypinam PIN {gpio_pin} pretoze aktualny primere teplot ({current_temp}) je mensi ako limit {limit_temperature} a FAN bezi')
    fan.write(gpio_pin, 0)
    return
  elif current_temp < limit_temperature and fan.read(gpio_pin) == 0:
    print(f'NEMENIM PIN {gpio_pin} pretoze aktualny primere teplot ({current_temp}) je mensi ako limit {limit_temperature} a FAN NEbezi')
    return
  else:
    print('Tento stav nemal nastat... netusim, co sa stalo')
    return

fan = pigpio.pi()

try:
  while True:
    sns = temp_check.Sensor(sensor_id)
    temp_store = memorydb.TemperatureStore(sensor_id)
    temperature, timestmp = sns.get_celsius()
    temp_store.add_value(temperature, timestmp)
    current_temp = temp_store.mean(retention)
    print(os.path.basename(sensor_id), ' ', current_temp)
    fanCheck(current_temp)
    time.sleep(interval)
finally:
  fan.write(gpio_pin, 0)
