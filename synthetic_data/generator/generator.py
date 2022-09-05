
from pydoc import classname


class SyntheticDataGenerator:

  msg = ""

  # TODO
  #  the constructor wants static file paths and models
  def _init__(self):
    self.msg = "SyntheticDataGenerator"

  def generate(self, n_patients: int, n_days: int=None):
    print("%s" % self.msg)
    print(" - num of patients: %d" % n_patients)
    if n_days is not None:
      print(" - num of patients: %d" % n_days)
