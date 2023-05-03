import datetime
class Checker:
  def __init__(self, var_type, value):
    self.var_type = var_type
    self.value = value
  def do_str(self):
    return str(self.value)
  def do_int(self):
    return int(self.value)
  def do_float(self):
    return float(self.value.replace(',','.'))
  def do_time(self):
    return datetime.datetime.strptime(self.value, '%H:%M:%S').time()
  def do_check(self):
    do = f'do_{self.var_type}'
    if hasattr(self, do) and callable(func := getattr(self, do)):
      return func()
