
class SyntheticDataEvaluator:

  msg = ""

  # TODO
  #  the constructor wants static file paths
  def _init__(self):
    self.msg = "SyntheticDataEvaluator"

  def evaluate(self, dataset):
    print("%s" % self.msg)
    print(" - dataset: %s" % dataset)
