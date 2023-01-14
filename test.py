import temp_check
import memorydb
import time
import glob
import os
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
  """)
while True:
  sns = temp_check.Sensor(sensor_id)
  temp_store = memorydb.TemperatureStore(sensor_id)
  temperature, timestmp = sns.get_celsius()
  temp_store.add_value(temperature, timestmp)
  print(os.path.basename(sensor_id), ' ',temp_store.mean(retention))
  time.sleep(interval)
