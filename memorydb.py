from tinydb import TinyDB, where, Query
from tinydb.storages import MemoryStorage
import datetime
import statistics
from time import sleep
db = TinyDB(storage=MemoryStorage)
q = Query()

class TemperatureStore:
  """
    TO DO:
     - menitelny pocet udrziavanich hodnot pri inicializacii classy
     - menitelny pocet hodnot z ktorych sa vyratava priemer
       - Pravdepodobne to budeme nastavovat na classe. Aby sa to drzalo pocas celej instancie
     - Vytvorime tabulku per sensor, nech sa to lahsie udrzuje
       - k tomu treba prisposobit citanie, zapisovanie a mazanie
  """
  
  def __init__(self, sensor_mac):
    self.sensor_mac = sensor_mac

  def mean(self):
    """
    Vrati priemernu hodnotu za N hodnot a odmaze to, co je navyse, aby sme udrziavali malo alokovanej pamate.
    """
    try:
      temp_array = [x['temp'] for x in db.all()[-5:]]
    except IndexError:
      print('Not enough resources')
    else:
      print(temp_array)
      avarage = statistics.mean(temp_array)
      try:
        db.remove(doc_ids=[x.doc_id for x in db.search(q.time < db.all()[-5]['time'])])
      except IndexError:
        print('Nothing to delete')
      return avarage

  def add_value(self, temperature, time = datetime.datetime.now()):
    db.insert({'sensor_mac': self.sensor_mac, 'time': time, 'temp': temperature})
