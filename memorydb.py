from tinydb import TinyDB, where, Query
from tinydb.storages import MemoryStorage
import datetime
import statistics
from time import sleep
db = TinyDB(storage=MemoryStorage)
q = Query()

class TemperatureStore:
  """
  """
  
  def __init__(self, sensor_mac):
    self.sensor_mac = sensor_mac
    self.table = db.table(sensor_mac)

  def mean(self, retention):
    """
    Vrati priemernu hodnotu za N hodnot a odmaze to, co je navyse, aby sme udrziavali malo alokovanej pamate.
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
    self.table.insert({'sensor_mac': self.sensor_mac, 'time': time, 'temp': temperature})
