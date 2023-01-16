from tinydb import TinyDB, where, Query
from tinydb.storages import MemoryStorage
import datetime
import statistics
from time import sleep


class TemperatureStore:
  """
  Here we store and maintain incoming values for storing temperature data.
  We can have instance for any number of sensors, becauces we create table in memory based on incoming sensor_id.
  """
  global db
  global q
  db = TinyDB(storage=MemoryStorage)
  q = Query()


  def __init__(self, sensor_mac):
    self.sensor_mac = sensor_mac
    self.table = db.table(sensor_mac)

  def mean(self, retention):
    """
    Returns mean value in N values and deletes what is above definued number of values.
    """
    try:
      temp_array = [x['temp'] for x in self.table.all()[-retention:]]
    except IndexError:
      print('Not enough resources')
    else:
      print(temp_array)
      avarage = statistics.mean(temp_array)
      try:
        self.table.remove(doc_ids=[x.doc_id for x in self.table.search(q.time < self.table.all()[-retention]['time'])])
      except IndexError:
        print('Nothing to delete')
      return avarage

  def add_value(self, temperature, time = datetime.datetime.now()):
    """
    Adding new value to memory table.
    """
    self.table.insert({'sensor_mac': self.sensor_mac, 'time': time, 'temp': temperature})
